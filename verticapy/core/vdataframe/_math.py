"""
(c)  Copyright  [2018-2023]  OpenText  or one of its
affiliates.  Licensed  under  the   Apache  License,
Version 2.0 (the  "License"); You  may  not use this
file except in compliance with the License.

You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0

Unless  required  by applicable  law or  agreed to in
writing, software  distributed  under the  License is
distributed on an  "AS IS" BASIS,  WITHOUT WARRANTIES
OR CONDITIONS OF ANY KIND, either express or implied.
See the  License for the specific  language governing
permissions and limitations under the License.
"""
import random
from typing import Literal, Union

from verticapy._typing import PythonNumber, PythonScalar, SQLColumns
from verticapy._utils._map import verticapy_agg_name
from verticapy._utils._sql._cast import to_category
from verticapy._utils._sql._collect import save_verticapy_logs
from verticapy._utils._sql._format import quote_ident
from verticapy.errors import MissingColumn, ParameterError, QueryError

from verticapy.core.string_sql.base import StringSQL

from verticapy.sql.dtypes import get_data_types
from verticapy.sql.functions.conditional import decode


class vDFMath:
    def __abs__(self):
        return self.copy().abs()

    def __ceil__(self, n):
        vdf = self.copy()
        columns = vdf.numcol()
        for elem in columns:
            if vdf[elem].category() == "float":
                vdf[elem].apply_fun(func="ceil", x=n)
        return vdf

    def __floor__(self, n):
        vdf = self.copy()
        columns = vdf.numcol()
        for elem in columns:
            if vdf[elem].category() == "float":
                vdf[elem].apply_fun(func="floor", x=n)
        return vdf

    def __len__(self):
        return int(self.shape()[0])

    def __nonzero__(self):
        return self.shape()[0] > 0 and not (self.empty())

    def __round__(self, n):
        vdf = self.copy()
        columns = vdf.numcol()
        for elem in columns:
            if vdf[elem].category() == "float":
                vdf[elem].apply_fun(func="round", x=n)
        return vdf

    @save_verticapy_logs
    def abs(self, columns: SQLColumns = []):
        """
    Applies the absolute value function to all input vDataColumns. 

    Parameters
    ----------
    columns: SQLColumns, optional
        List of the vDataColumns names. If empty, all numerical vDataColumns will 
        be used.

    Returns
    -------
    vDataFrame
        self

    See Also
    --------
    vDataFrame.apply    : Applies functions to the input vDataColumns.
    vDataFrame.applymap : Applies a function to all vDataColumns.
        """
        if isinstance(columns, str):
            columns = [columns]
        columns = self.numcol() if not (columns) else self._format_colnames(columns)
        func = {}
        for column in columns:
            if not (self[column].isbool()):
                func[column] = "ABS({})"
        return self.apply(func)

    @save_verticapy_logs
    def analytic(
        self,
        func: str,
        columns: SQLColumns = [],
        by: SQLColumns = [],
        order_by: Union[dict, list] = [],
        name: str = "",
        offset: int = 1,
        x_smoothing: float = 0.5,
        add_count: bool = True,
    ):
        """
    Adds a new vDataColumn to the vDataFrame by using an advanced analytical 
    function on one or two specific vDataColumns.

    \u26A0 Warning : Some analytical functions can make the vDataFrame 
                     structure more resource intensive. It is best to check 
                     the structure of the vDataFrame using the 'current_relation' 
                     method and to save it using the 'to_db' method with 
                     the parameters 'inplace = True' and 
                     'relation_type = table'

    Parameters
    ----------
    func: str
        Function to apply.
            aad          : average absolute deviation
            beta         : Beta Coefficient between 2 vDataColumns
            count        : number of non-missing elements
            corr         : Pearson's correlation between 2 vDataColumns
            cov          : covariance between 2 vDataColumns
            dense_rank   : dense rank
            ema          : exponential moving average
            first_value  : first non null lead
            iqr          : interquartile range
            kurtosis     : kurtosis
            jb           : Jarque-Bera index 
            lead         : next element
            lag          : previous element
            last_value   : first non null lag
            mad          : median absolute deviation
            max          : maximum
            mean         : average
            median       : median
            min          : minimum
            mode         : most occurent element
            q%           : q quantile (ex: 50% for the median)
            pct_change   : ratio between the current value and the previous one
            percent_rank : percent rank
            prod         : product
            range        : difference between the max and the min
            rank         : rank
            row_number   : row number
            sem          : standard error of the mean
            skewness     : skewness
            sum          : sum
            std          : standard deviation
            unique       : cardinality (count distinct)
            var          : variance
                Other analytical functions could work if it is part of 
                the DB version you are using.
    columns: SQLColumns, optional
        Input vDataColumns. It can be a list of one or two elements.
    by: SQLColumns, optional
        vDataColumns used in the partition.
    order_by: dict / list, optional
        List of the vDataColumns to use to sort the data using asc order or
        dictionary of all sorting methods. For example, to sort by "column1"
        ASC and "column2" DESC, write {"column1": "asc", "column2": "desc"}
    name: str, optional
        Name of the new vDataColumn. If empty a default name based on the other
        parameters will be generated.
    offset: int, optional
        Lead/Lag offset if parameter 'func' is the function 'lead'/'lag'.
    x_smoothing: float, optional
        The smoothing parameter of the 'ema' if the function is 'ema'. It must be in [0;1]
    add_count: bool, optional
        If the function is the 'mode' and this parameter is True then another column will 
        be added to the vDataFrame with the mode number of occurences.

    Returns
    -------
    vDataFrame
        self

    See Also
    --------
    vDataFrame.eval    : Evaluates a customized expression.
    vDataFrame.rolling : Computes a customized moving window.
        """
        if isinstance(by, str):
            by = [by]
        if isinstance(order_by, str):
            order_by = [order_by]
        if isinstance(columns, str):
            if columns:
                columns = [columns]
            else:
                columns = []
        columns, by = self._format_colnames(columns, by)
        by_name = ["by"] + by if (by) else []
        by_order = ["order_by"] + [elem for elem in order_by] if (order_by) else []
        if not (name):
            name = gen_name([func] + columns + by_name + by_order)
        func = func.lower()
        by = ", ".join(by)
        by = f"PARTITION BY {by}" if (by) else ""
        order_by = self._get_sort_syntax(order_by)
        func = verticapy_agg_name(func.lower(), method="vertica")
        if func in (
            "max",
            "min",
            "avg",
            "sum",
            "count",
            "stddev",
            "median",
            "variance",
            "unique",
            "top",
            "kurtosis",
            "skewness",
            "mad",
            "aad",
            "range",
            "prod",
            "jb",
            "iqr",
            "sem",
        ) or ("%" in func):
            if order_by and not (conf.get_option("print_info")):
                print(
                    f"\u26A0 '{func}' analytic method doesn't need an "
                    "order by clause, it was ignored"
                )
            elif not (columns):
                raise MissingColumn(
                    "The parameter 'column' must be a vDataFrame Column "
                    f"when using analytic method '{func}'"
                )
            if func in ("skewness", "kurtosis", "aad", "mad", "jb"):
                random_nb = random.randint(0, 10000000)
                column_str = columns[0].replace('"', "")
                mean_name = f"{column_str}_mean_{random_nb}"
                median_name = f"{column_str}_median_{random_nb}"
                std_name = f"{column_str}_std_{random_nb}"
                count_name = f"{column_str}_count_{random_nb}"
                all_cols = [elem for elem in self._vars["columns"]]
                if func == "mad":
                    self.eval(median_name, f"MEDIAN({columns[0]}) OVER ({by})")
                else:
                    self.eval(mean_name, f"AVG({columns[0]}) OVER ({by})")
                if func not in ("aad", "mad"):
                    self.eval(std_name, f"STDDEV({columns[0]}) OVER ({by})")
                    self.eval(count_name, f"COUNT({columns[0]}) OVER ({by})")
                if func == "kurtosis":
                    self.eval(
                        name,
                        f"""AVG(POWER(({columns[0]} - {mean_name}) 
                          / NULLIFZERO({std_name}), 4)) OVER ({by}) 
                          * POWER({count_name}, 2) 
                          * ({count_name} + 1) 
                          / NULLIFZERO(({count_name} - 1) 
                          * ({count_name} - 2) 
                          * ({count_name} - 3)) 
                          - 3 * POWER({count_name} - 1, 2) 
                          / NULLIFZERO(({count_name} - 2) 
                          * ({count_name} - 3))""",
                    )
                elif func == "skewness":
                    self.eval(
                        name,
                        f"""AVG(POWER(({columns[0]} - {mean_name}) 
                         / NULLIFZERO({std_name}), 3)) OVER ({by}) 
                         * POWER({count_name}, 2) 
                         / NULLIFZERO(({count_name} - 1) 
                         * ({count_name} - 2))""",
                    )
                elif func == "jb":
                    self.eval(
                        name,
                        f"""{count_name} / 6 * (POWER(AVG(POWER(({columns[0]} 
                          - {mean_name}) / NULLIFZERO({std_name}), 3)) OVER ({by}) 
                          * POWER({count_name}, 2) / NULLIFZERO(({count_name} - 1) 
                          * ({count_name} - 2)), 2) + POWER(AVG(POWER(({columns[0]} 
                          - {mean_name}) / NULLIFZERO({std_name}), 4)) OVER ({by}) 
                          * POWER({count_name}, 2) * ({count_name} + 1) 
                          / NULLIFZERO(({count_name} - 1) * ({count_name} - 2) 
                          * ({count_name} - 3)) - 3 * POWER({count_name} - 1, 2) 
                          / NULLIFZERO(({count_name} - 2) * ({count_name} - 3)), 2) / 4)""",
                    )
                elif func == "aad":
                    self.eval(
                        name, f"AVG(ABS({columns[0]} - {mean_name})) OVER ({by})",
                    )
                elif func == "mad":
                    self.eval(
                        name, f"AVG(ABS({columns[0]} - {median_name})) OVER ({by})",
                    )
            elif func == "top":
                if not (by):
                    by_str = f"PARTITION BY {columns[0]}"
                else:
                    by_str = f"{by}, {columns[0]}"
                self.eval(name, f"ROW_NUMBER() OVER ({by_str})")
                if add_count:
                    name_str = name.replace('"', "")
                    self.eval(
                        f"{name_str}_count",
                        f"NTH_VALUE({name}, 1) OVER ({by} ORDER BY {name} DESC)",
                    )
                self[name].apply(
                    f"NTH_VALUE({columns[0]}, 1) OVER ({by} ORDER BY {{}} DESC)"
                )
            elif func == "unique":
                self.eval(
                    name,
                    f"""DENSE_RANK() OVER ({by} ORDER BY {columns[0]} ASC) 
                      + DENSE_RANK() OVER ({by} ORDER BY {columns[0]} DESC) - 1""",
                )
            elif "%" == func[-1]:
                try:
                    x = float(func[0:-1]) / 100
                except:
                    raise FunctionError(
                        f"The aggregate function '{fun}' doesn't exist. "
                        "If you want to compute the percentile x of the "
                        "element please write 'x%' with x > 0. Example: "
                        "50% for the median."
                    )
                self.eval(
                    name,
                    f"PERCENTILE_CONT({x}) WITHIN GROUP(ORDER BY {columns[0]}) OVER ({by})",
                )
            elif func == "range":
                self.eval(
                    name,
                    f"MAX({columns[0]}) OVER ({by}) - MIN({columns[0]}) OVER ({by})",
                )
            elif func == "iqr":
                self.eval(
                    name,
                    f"""PERCENTILE_CONT(0.75) WITHIN GROUP(ORDER BY {columns[0]}) OVER ({by}) 
                      - PERCENTILE_CONT(0.25) WITHIN GROUP(ORDER BY {columns[0]}) OVER ({by})""",
                )
            elif func == "sem":
                self.eval(
                    name,
                    f"STDDEV({columns[0]}) OVER ({by}) / SQRT(COUNT({columns[0]}) OVER ({by}))",
                )
            elif func == "prod":
                self.eval(
                    name,
                    f"""DECODE(ABS(MOD(SUM(CASE 
                                            WHEN {columns[0]} < 0 
                                            THEN 1 ELSE 0 END) 
                                       OVER ({by}), 2)), 0, 1, -1) 
                     * POWER(10, SUM(LOG(ABS({columns[0]}))) 
                                 OVER ({by}))""",
                )
            else:
                self.eval(name, f"{func.upper()}({columns[0]}) OVER ({by})")
        elif func in (
            "lead",
            "lag",
            "row_number",
            "percent_rank",
            "dense_rank",
            "rank",
            "first_value",
            "last_value",
            "exponential_moving_average",
            "pct_change",
        ):
            if not (columns) and func in (
                "lead",
                "lag",
                "first_value",
                "last_value",
                "pct_change",
            ):
                raise ParameterError(
                    "The parameter 'columns' must be a vDataFrame column when "
                    f"using analytic method '{func}'"
                )
            elif (columns) and func not in (
                "lead",
                "lag",
                "first_value",
                "last_value",
                "pct_change",
                "exponential_moving_average",
            ):
                raise ParameterError(
                    "The parameter 'columns' must be empty when using analytic"
                    f" method '{func}'"
                )
            if (by) and (order_by):
                order_by = f" {order_by}"
            if func in ("lead", "lag"):
                info_param = f", {offset}"
            elif func in ("last_value", "first_value"):
                info_param = " IGNORE NULLS"
            elif func == "exponential_moving_average":
                info_param = f", {x_smoothing}"
            else:
                info_param = ""
            if func == "pct_change":
                self.eval(
                    name, f"{columns[0]} / (LAG({columns[0]}) OVER ({by}{order_by}))",
                )
            else:
                columns0 = columns[0] if (columns) else ""
                self.eval(
                    name,
                    f"{func.upper()}({columns0}{info_param}) OVER ({by}{order_by})",
                )
        elif func in ("corr", "cov", "beta"):
            if order_by:
                print(
                    f"\u26A0 '{func}' analytic method doesn't need an "
                    "order by clause, it was ignored"
                )
            assert len(columns) == 2, MissingColumn(
                "The parameter 'columns' includes 2 vDataColumns when using "
                f"analytic method '{func}'"
            )
            if columns[0] == columns[1]:
                if func == "cov":
                    expr = f"VARIANCE({columns[0]}) OVER ({by})"
                else:
                    expr = 1
            else:
                if func == "corr":
                    den = f" / (STDDEV({columns[0]}) OVER ({by}) * STDDEV({columns[1]}) OVER ({by}))"
                elif func == "beta":
                    den = f" / (VARIANCE({columns[1]}) OVER ({by}))"
                else:
                    den = ""
                expr = f"""
                    (AVG({columns[0]} * {columns[1]}) OVER ({by}) 
                   - AVG({columns[0]}) OVER ({by}) 
                   * AVG({columns[1]}) OVER ({by})){den}"""
            self.eval(name, expr)
        else:
            try:
                self.eval(
                    name,
                    f"{func.upper()}({columns[0]}{info_param}) OVER ({by}{order_by})",
                )
            except:
                raise FunctionError(
                    f"The aggregate function '{func}' doesn't exist or is not "
                    "managed by the 'analytic' method. If you want more "
                    "flexibility use the 'eval' method."
                )
        if func in ("kurtosis", "skewness", "jb"):
            self._vars["exclude_columns"] += [
                quote_ident(mean_name),
                quote_ident(std_name),
                quote_ident(count_name),
            ]
        elif func == "aad":
            self._vars["exclude_columns"] += [quote_ident(mean_name)]
        elif func == "mad":
            self._vars["exclude_columns"] += [quote_ident(median_name)]
        return self

    @save_verticapy_logs
    def apply(self, func: dict):
        """
    Applies each function of the dictionary to the input vDataColumns.

    Parameters
     ----------
     func: dict
        Dictionary of functions.
        The dictionary must be like the following: 
        {column1: func1, ..., columnk: funck}. Each function variable must
        be composed of two flower brackets {}. For example to apply the 
        function: x -> x^2 + 2 use "POWER({}, 2) + 2".

     Returns
     -------
     vDataFrame
        self

    See Also
    --------
    vDataFrame.applymap : Applies a function to all vDataColumns.
    vDataFrame.eval     : Evaluates a customized expression.
        """
        func = self._format_colnames(func)
        for column in func:
            self[column].apply(func[column])
        return self

    @save_verticapy_logs
    def applymap(self, func: str, numeric_only: bool = True):
        """
    Applies a function to all vDataColumns. 

    Parameters
    ----------
    func: str
        The function.
        The function variable must be composed of two flower brackets {}. 
        For example to apply the function: x -> x^2 + 2 use "POWER({}, 2) + 2".
    numeric_only: bool, optional
        If set to True, only the numerical columns will be used.

    Returns
    -------
    vDataFrame
        self

    See Also
    --------
    vDataFrame.apply : Applies functions to the input vDataColumns.
        """
        function = {}
        columns = self.numcol() if numeric_only else self.get_columns()
        for column in columns:
            function[column] = (
                func if not (self[column].isbool()) else func.replace("{}", "{}::int")
            )
        return self.apply(function)

    @save_verticapy_logs
    def case_when(self, name: str, *args):
        """
    Creates a new feature by evaluating some conditions.
    
    Parameters
    ----------
    name: str
        Name of the new feature.
    args: object
        Infinite Number of Expressions.
        The expression generated will look like:
        even: CASE ... WHEN args[2 * i] THEN args[2 * i + 1] ... END
        odd : CASE ... WHEN args[2 * i] THEN args[2 * i + 1] ... ELSE args[n] END

    Returns
    -------
    vDataFrame
        self
    
    See Also
    --------
    vDataFrame[].decode : Encodes the vDataColumn using a User Defined Encoding.
    vDataFrame.eval : Evaluates a customized expression.
        """
        from verticapy.sql.functions import case_when

        return self.eval(name=name, expr=case_when(*args))


class vDCMath:
    def __len__(self):
        return int(self.count())

    def __nonzero__(self):
        return self.count() > 0

    @save_verticapy_logs
    def abs(self):
        """
    Applies the absolute value function to the input vDataColumn. 

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame[].apply : Applies a function to the input vDataColumn.
        """
        return self.apply(func="ABS({})")

    @save_verticapy_logs
    def add(self, x: PythonNumber):
        """
    Adds the input element to the vDataColumn.

    Parameters
    ----------
    x: float
        If the vDataColumn type is date like (date, datetime ...), the parameter 'x' 
        will represent the number of seconds, otherwise it will represent a number.

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame[].apply : Applies a function to the input vDataColumn.
        """
        if self.isdate():
            return self.apply(func=f"TIMESTAMPADD(SECOND, {x}, {{}})")
        else:
            return self.apply(func=f"{{}} + ({x})")

    @save_verticapy_logs
    def apply(self, func: Union[str, StringSQL], copy_name: str = ""):
        """
    Applies a function to the vDataColumn.

    Parameters
    ----------
    func: str,
        Function in pure SQL used to transform the vDataColumn.
        The function variable must be composed of two flower brackets {}. For 
        example to apply the function: x -> x^2 + 2 use "POWER({}, 2) + 2".
    copy_name: str, optional
        If not empty, a copy will be created using the input Name.

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame.apply    : Applies functions to the input vDataColumns.
    vDataFrame.applymap : Applies a function to all the vDataColumns.
    vDataFrame.eval     : Evaluates a customized expression.
        """
        if isinstance(func, StringSQL):
            func = str(func)
        func_apply = func.replace("{}", self._alias)
        alias_sql_repr = self._alias.replace('"', "")
        try:
            ctype = get_data_types(
                expr=f"""
                    SELECT 
                        {func_apply} AS apply_test_feature 
                    FROM {self._parent._genSQL()} 
                    WHERE {self._alias} IS NOT NULL 
                    LIMIT 0""",
                column="apply_test_feature",
            )
            category = to_category(ctype=ctype)
            all_cols, max_floor = self._parent.get_columns(), 0
            for column in all_cols:
                try:
                    column_str = column.replace('"', "")
                    if (quote_ident(column) in func) or (
                        re.search(re.compile(f"\\b{column_str}\\b"), func,)
                    ):
                        max_floor = max(len(self._parent[column]._transf), max_floor)
                except:
                    pass
            max_floor -= len(self._transf)
            if copy_name:
                copy_name_str = copy_name.replace('"', "")
                self.add_copy(name=copy_name)
                for k in range(max_floor):
                    self._parent[copy_name]._transf += [
                        ("{}", self.ctype(), self.category())
                    ]
                self._parent[copy_name]._transf += [(func, ctype, category)]
                self._parent[copy_name]._catalog = self._catalog
            else:
                for k in range(max_floor):
                    self._transf += [("{}", self.ctype(), self.category())]
                self._transf += [(func, ctype, category)]
                self._parent._update_catalog(erase=True, columns=[self._alias])
            self._parent._add_to_history(
                f"[Apply]: The vDataColumn '{alias_sql_repr}' was "
                f"transformed with the func 'x -> {func_apply}'."
            )
            return self._parent
        except Exception as e:
            raise QueryError(
                f"{e}\nError when applying the func 'x -> {func_apply}' "
                f"to '{alias_sql_repr}'"
            )

    @save_verticapy_logs
    def apply_fun(
        self,
        func: Literal[
            "abs",
            "acos",
            "asin",
            "atan",
            "avg",
            "cbrt",
            "ceil",
            "contain",
            "count",
            "cos",
            "cosh",
            "cot",
            "dim",
            "exp",
            "find",
            "floor",
            "len",
            "length",
            "ln",
            "log",
            "log10",
            "max",
            "mean",
            "mod",
            "min",
            "pow",
            "round",
            "sign",
            "sin",
            "sinh",
            "sum",
            "sqrt",
            "tan",
            "tanh",
        ],
        x: PythonScalar = 2,
    ):
        """
    Applies a default function to the vDataColumn.

    Parameters
    ----------
    func: str
        Function to use to transform the vDataColumn.
            abs          : absolute value
            acos         : trigonometric inverse cosine
            asin         : trigonometric inverse sine
            atan         : trigonometric inverse tangent
            avg / mean   : average
            cbrt         : cube root
            ceil         : value up to the next whole number
            contain      : checks if 'x' is in the collection
            count        : number of non-null elements
            cos          : trigonometric cosine
            cosh         : hyperbolic cosine
            cot          : trigonometric cotangent
            dim          : dimension (only for arrays)
            exp          : exponential function
            find         : returns the ordinal position of a specified element 
                           in an array (only for arrays)
            floor        : value down to the next whole number
            len / length : length
            ln           : natural logarithm
            log          : logarithm
            log10        : base 10 logarithm
            max          : maximum
            min          : minimum
            mod          : remainder of a division operation
            pow          : number raised to the power of another number
            round        : rounds a value to a specified number of decimal places
            sign         : arithmetic sign
            sin          : trigonometric sine
            sinh         : hyperbolic sine
            sqrt         : arithmetic square root
            sum          : sum
            tan          : trigonometric tangent
            tanh         : hyperbolic tangent
    x: PythonScalar, optional
        If the function has two arguments (example, power or mod), 'x' represents 
        the second argument.

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame[].apply : Applies a function to the vDataColumn.
        """
        if func == "mean":
            func = "avg"
        elif func == "length":
            func = "len"
        cat = self.category()
        if func == "len":
            if cat == "vmap":
                func = "MAPSIZE"
            elif cat == "complex":
                func = "APPLY_COUNT_ELEMENTS"
            else:
                func = "LENTGH"
        elif func in ("max", "min", "sum", "avg", "count"):
            func = "APPLY_" + func
        elif func == "dim":
            func = "ARRAY_DIMS"
        if func not in ("log", "mod", "pow", "round", "contain", "find"):
            expr = f"{func.upper()}({{}})"
        elif func in ("log", "mod", "pow", "round"):
            expr = f"{func.upper()}({{}}, {x})"
        elif func in ("contain", "find"):
            if func == "contain":
                if cat == "vmap":
                    f = "MAPCONTAINSVALUE"
                else:
                    f = "CONTAINS"
            elif func == "find":
                f = "ARRAY_FIND"
            if isinstance(x, str):
                x = "'" + str(x).replace("'", "''") + "'"
            expr = f"{f}({{}}, {x})"
        return self.apply(func=expr)

    @save_verticapy_logs
    def date_part(self, field: str):
        """
    Extracts a specific TS field from the vDataColumn (only if the vDataColumn type is 
    date like). The vDataColumn will be transformed.

    Parameters
    ----------
    field: str
        The field to extract. It must be one of the following: 
        CENTURY / DAY / DECADE / DOQ / DOW / DOY / EPOCH / HOUR / ISODOW / ISOWEEK /
        ISOYEAR / MICROSECONDS / MILLENNIUM / MILLISECONDS / MINUTE / MONTH / QUARTER / 
        SECOND / TIME ZONE / TIMEZONE_HOUR / TIMEZONE_MINUTE / WEEK / YEAR

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame[].slice : Slices the vDataColumn using a time series rule.
        """
        return self.apply(func=f"DATE_PART('{field}', {{}})")

    @save_verticapy_logs
    def decode(self, *args):
        """
    Encodes the vDataColumn using a user-defined encoding.

    Parameters
    ----------
    args: object
        Any amount of expressions.
        The expression generated will look like:
        even: CASE ... WHEN vDataColumn = args[2 * i] THEN args[2 * i + 1] ... END
        odd : CASE ... WHEN vDataColumn = args[2 * i] THEN args[2 * i + 1] ... ELSE args[n] END

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame.case_when      : Creates a new feature by evaluating some conditions.
    vDataFrame[].discretize   : Discretizes the vDataColumn.
    vDataFrame[].label_encode : Encodes the vDataColumn with Label Encoding.
    vDataFrame[].get_dummies  : Encodes the vDataColumn with One-Hot Encoding.
    vDataFrame[].mean_encode  : Encodes the vDataColumn using the mean encoding of a response.
        """
        return self.apply(func=decode(StringSQL("{}"), *args))

    @save_verticapy_logs
    def div(self, x: PythonNumber):
        """
    Divides the vDataColumn by the input element.

    Parameters
    ----------
    x: PythonNumber
        Input number.

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame[].apply : Applies a function to the input vDataColumn.
        """
        assert x != 0, ValueError("Division by 0 is forbidden !")
        return self.apply(func=f"{{}} / ({x})")

    def get_len(self):
        """
    Returns a new vDataColumn that represents the length of each element.

    Returns
    -------
    vDataColumn
        vDataColumn that includes the length of each element.
        """
        cat = self.category()
        if cat == "vmap":
            fun = "MAPSIZE"
        elif cat == "complex":
            fun = "APPLY_COUNT_ELEMENTS"
        else:
            fun = "LENGTH"
        elem_to_select = f"{fun}({self._alias})"
        init_transf = f"{fun}({self._init_transf})"
        new_alias = quote_ident(self._alias[1:-1] + ".length")
        query = f"""
            SELECT 
                {elem_to_select} AS {new_alias} 
            FROM {self._parent._genSQL()}"""
        vcol = self._parent._new_vdataframe(query)[new_alias]
        vcol._init_transf = init_transf
        return vcol

    @save_verticapy_logs
    def round(self, n: int):
        """
    Rounds the vDataColumn by keeping only the input number of digits after the comma.

    Parameters
    ----------
    n: int
        Number of digits to keep after the comma.

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame[].apply : Applies a function to the input vDataColumn.
        """
        return self.apply(func=f"ROUND({{}}, {n})")

    @save_verticapy_logs
    def slice(self, length: int, unit: str = "second", start: bool = True):
        """
    Slices and transforms the vDataColumn using a time series rule.

    Parameters
    ----------
    length: int
        Slice size.
    unit: str, optional
        Slice size unit. For example, it can be 'minute' 'hour'...
    start: bool, optional
        If set to True, the record will be sliced using the floor of the slicing
        instead of the ceiling.

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame[].date_part : Extracts a specific TS field from the vDataColumn.
        """
        start_or_end = "START" if (start) else "END"
        unit = unit.upper()
        return self.apply(
            func=f"TIME_SLICE({{}}, {length}, '{unit}', '{start_or_end}')"
        )

    @save_verticapy_logs
    def sub(self, x: PythonNumber):
        """
    Subtracts the input element from the vDataColumn.

    Parameters
    ----------
    x: PythonNumber
        If the vDataColumn type is date like (date, datetime ...), the parameter 'x' 
        will represent the number of seconds, otherwise it will represent a number.

    Returns
    -------
    vDataFrame
        self._parent

    See Also
    --------
    vDataFrame[].apply : Applies a function to the input vDataColumn.
        """
        if self.isdate():
            return self.apply(func=f"TIMESTAMPADD(SECOND, -({x}), {{}})")
        else:
            return self.apply(func=f"{{}} - ({x})")