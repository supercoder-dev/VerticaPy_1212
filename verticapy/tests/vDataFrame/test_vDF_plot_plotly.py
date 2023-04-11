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

# Pytest
import pytest

# Standard Python Modules
import datetime, os, sys, random

# Other Modules
import plotly.express as px
import plotly
import pandas as pd
import numpy as np
import scipy

# VerticaPy
import verticapy
import verticapy._config.config as conf
from verticapy import drop
from verticapy.datasets import load_titanic, load_iris, load_amazon

from verticapy.learn.linear_model import LinearRegression
from verticapy.learn.model_selection import elbow


conf.set_option("print_info", False)


@pytest.fixture(scope="module")
def dummy_vd():
    arr1 = np.concatenate((np.ones(60), np.zeros(40))).astype(int)
    np.random.shuffle(arr1)
    arr2 = np.concatenate((np.repeat("A", 20), np.repeat("B", 30), np.repeat("C", 50)))
    np.random.shuffle(arr2)
    dummy = verticapy.vDataFrame(list(zip(arr1, arr2)), ["check 1", "check 2"])
    yield dummy


@pytest.fixture(scope="module")
def dummy_scatter_vd():
    slope = 10
    y_intercept = -20
    scatter_magnitude = 4
    x = np.linspace(0, 10, 100)
    y = y_intercept + slope * x + np.random.randn(100) * scatter_magnitude
    dummy = verticapy.vDataFrame({"x": x, "y": y})
    yield dummy


@pytest.fixture(scope="module")
def dummy_date_vd():
    N = 100
    years = [1910, 1920, 1930, 1940, 1950]
    median = 500
    q1 = 200
    q3 = 800
    std = (q3 - q1) / (2 * np.sqrt(2) * scipy.special.erfinv(0.5))
    data = np.random.normal(median, std, N)
    dummy = pd.DataFrame(
        {"date": [1910, 1920, 1930, 1940, 1950] * int(N / 5), "value": list(data),}
    )
    dummy = verticapy.vDataFrame(dummy)
    yield dummy


@pytest.fixture(scope="module")
def dummy_dist_vd():
    N = 1000
    ones_percentage = 0.4
    median = 50
    q1 = 40
    q3 = 60
    percentage_A = 0.4
    percentage_B = 0.3
    percentage_C = 1 - (percentage_A + percentage_B)
    categories = ["A", "B", "C"]
    category_array = np.random.choice(
        categories, size=N, p=[percentage_A, percentage_B, percentage_C]
    )
    category_array = category_array.reshape(len(category_array), 1)
    zeros_array = np.zeros(int(N * (1 - ones_percentage)))
    ones_array = np.ones(int(N * ones_percentage))
    result_array = np.concatenate((zeros_array, ones_array))
    np.random.shuffle(result_array)
    result_array = result_array.reshape(len(result_array), 1)
    std = (q3 - q1) / (2 * np.sqrt(2) * scipy.special.erfinv(0.5))
    data = np.random.normal(median, std, N)
    data = data.reshape(len(data), 1)
    cols_combined = np.concatenate((data, result_array, category_array), axis=1)
    data_all = pd.DataFrame(cols_combined, columns=["0", "binary", "cats"])
    dummy = verticapy.vDataFrame(data_all)
    dummy["binary"].astype("int")
    yield dummy


@pytest.fixture(scope="module")
def acf_plot_result(load_plotly, amazon_vd):
    return amazon_vd.acf(
        ts="date", column="number", p=12, by=["state"], unit="month", method="spearman",
    )


@pytest.fixture(scope="module")
def regression_plot_result(load_plotly, dummy_scatter_vd):
    model = LinearRegression("LR_churn")
    model.fit(dummy_scatter_vd, ["x"], "y")
    return model.plot()


@pytest.fixture(scope="module")
def titanic_vd():
    titanic = load_titanic()
    yield titanic
    drop(name="public.titanic")


@pytest.fixture(scope="module")
def elbow_plot_result(load_plotly, iris_vd):
    return elbow(input_relation=iris_vd, X=["PetalLengthCm", "PetalWidthCm"])


@pytest.fixture(scope="module")
def iris_vd():
    iris = load_iris()
    yield iris
    drop(name="public.iris")


@pytest.fixture(scope="module")
def amazon_vd():
    amazon = load_amazon()
    yield amazon
    drop(name="public.amazon")


@pytest.fixture(scope="module")
def load_plotly():
    conf.set_option("plotting_lib", "plotly")
    yield
    conf.set_option("plotting_lib", "matplotlib")


class TestvDFPlotPlotly:
    def test_vDF_bar(self, titanic_vd, load_plotly):
        # 1D bar charts

        ## Checking plotting library
        assert conf.get_option("plotting_lib") == "plotly"
        survived_values = titanic_vd.to_pandas()["survived"]

        ## Creating a test figure to compare
        test_fig = px.bar(
            x=[0, 1],
            y=[
                survived_values[survived_values == 0].count(),
                survived_values[survived_values == 1].count(),
            ],
        )
        test_fig = test_fig.update_xaxes(type="category")
        result = titanic_vd["survived"].bar()

        ## Testing Plot Properties
        ### Checking if correct object is created
        assert type(result) == plotly.graph_objs._figure.Figure
        ### Checking if the x-axis is a category instead of integer
        assert result.layout["xaxis"]["type"] == "category"

        ## Testing Data
        ### Comparing result with a test figure
        assert (
            result.data[0]["y"][np.where(result.data[0]["x"] == "0")[0][0]]
            / result.data[0]["y"][np.where(result.data[0]["x"] == "1")[0][0]]
            == test_fig.data[0]["y"][np.where(test_fig.data[0]["x"] == 0)[0][0]]
            / test_fig.data[0]["y"][np.where(test_fig.data[0]["x"] == 1)[0][0]]
        )

        ## Testing Additional Options
        ### Testing keyword arguments (kwargs)
        result = titanic_vd["survived"].bar(xaxis_title="Custom X Axis Title")
        assert result.layout["xaxis"]["title"]["text"] == "Custom X Axis Title"
        result = titanic_vd["survived"].bar(yaxis_title="Custom Y Axis Title")
        assert result.layout["yaxis"]["title"]["text"] == "Custom Y Axis Title"

    def test_vDF_pie(self, dummy_vd, load_plotly):
        # 1D pie charts

        ## Creating a pie chart
        result = dummy_vd["check 1"].pie()

        ## Testing Data
        ### check value corresponding to 0s
        assert (
            result.data[0]["values"][0]
            == dummy_vd[dummy_vd["check 1"] == 0]["check 1"].count()
            / dummy_vd["check 1"].count()
        )
        ### check value corresponding to 1s
        assert (
            result.data[0]["values"][1]
            == dummy_vd[dummy_vd["check 1"] == 1]["check 1"].count()
            / dummy_vd["check 1"].count()
        )

        ## Testing Plot Properties
        ### checking the label
        assert result.data[0]["labels"] == ("0", "1")
        ### check title
        assert result.layout["title"]["text"] == "check 1"

        ## Testing Additional Options
        ### check hole option
        result = dummy_vd["check 1"].pie(kind="donut")
        assert result.data[0]["hole"] == 0.2
        ### check exploded option
        result = dummy_vd["check 1"].pie(exploded=True)
        assert len(result.data[0]["pull"]) > 0

    def test_vDF_barh(self, dummy_vd, load_plotly):
        # 1D horizontal bar charts

        ## Creating horizontal bar chart
        result = dummy_vd["check 2"].barh()
        ## Testing Plot Properties
        ### Checking if correct object is created
        assert type(result) == plotly.graph_objs._figure.Figure
        ### Checking if the x-axis is a category instead of integer
        assert result.layout["yaxis"]["type"] == "category"

        ## Testing Data
        ### Comparing total adds up to 1
        assert sum(result.data[0]["x"]) == 1
        ### Checking if all labels are inlcuded
        assert set(result.data[0]["y"]).issubset(set(["A", "B", "C"]))
        ### Checking if the density was plotted correctly
        nums = dummy_vd.to_pandas()["check 2"].value_counts()
        total = len(dummy_vd)
        assert set(result.data[0]["x"]).issubset(
            set([nums["A"] / total, nums["B"] / total, nums["C"] / total])
        )

        ## Testing Additional Options
        ### Testing keyword arguments (kwargs)
        result = dummy_vd["check 2"].barh(xaxis_title="Custom X Axis Title")
        assert result.layout["xaxis"]["title"]["text"] == "Custom X Axis Title"
        result = dummy_vd["check 2"].barh(yaxis_title="Custom Y Axis Title")
        assert result.layout["yaxis"]["title"]["text"] == "Custom Y Axis Title"


class TestVDFNestedPieChart:
    def test_properties_type(self, load_plotly, dummy_vd):
        # Arrange
        # Act
        result = dummy_vd.pie(["check 1", "check 2"])
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure

    def test_properties_branch_values(self, load_plotly, dummy_vd):
        # Arrange
        # Act
        result = dummy_vd.pie(["check 1", "check 2"])
        # Assert - checking if the branch values are covering all
        assert result.data[0]["branchvalues"] == "total"

    def test_data_all_labels_for_nested(self, load_plotly, dummy_vd):
        # Arrange
        result = dummy_vd.pie(["check 1", "check 2"])
        # Act
        # Assert - checking if all the labels exist
        assert set(result.data[0]["labels"]) == {"1", "0", "A", "B", "C"}

    def test_data_all_labels_for_simple_pie(self, load_plotly, dummy_vd):
        # Arrange
        result = dummy_vd.pie(["check 1"])
        # Act
        # Assert - checking if all the labels exist for a simple pie plot
        assert set(result.data[0]["labels"]) == {"1", "0"}

    def test_data_check_parent_of_A(self, load_plotly, dummy_vd):
        # Arrange
        result = dummy_vd.pie(["check 1", "check 2"])
        # Act
        # Assert - checking the parent of 'A' which is an element of column "check 2"
        assert result.data[0]["parents"][result.data[0]["labels"].index("A")] in [
            "0",
            "1",
        ]

    def test_data_check_parent_of_0(self, load_plotly, dummy_vd):
        # Arrange
        result = dummy_vd.pie(["check 1", "check 2"])
        # Act
        # Assert - checking the parent of '0' which is an element of column "check 1"
        assert result.data[0]["parents"][result.data[0]["labels"].index("0")] in [""]

    def test_data_add_up_all_0s_from_children(self, load_plotly, dummy_vd):
        # Arrange
        # Act
        result = dummy_vd.pie(["check 1", "check 2"])
        zero_indices = [i for i, x in enumerate(result.data[0]["parents"]) if x == "0"]
        # Assert - checking if if all the children elements of 0 add up to its count
        assert sum([list(result.data[0]["values"])[i] for i in zero_indices]) == 40


class TestVDFScatterPlot:
    def test_properties_output_type(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm"])
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_xaxis_title(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm"])
        # Assert
        assert (
            result.layout["xaxis"]["title"]["text"] == "SepalWidthCm"
        ), "X-axis title issue"

    def test_properties_yaxis_title(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm"])
        # Assert
        assert (
            result.layout["yaxis"]["title"]["text"] == "SepalLengthCm"
        ), "Y-axis title issue"

    def test_properties_xaxis_title_3D_plot(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm", "PetalLengthCm"])
        # Assert
        assert (
            result.layout["scene"]["xaxis"]["title"]["text"] == "SepalWidthCm"
        ), "X-axis title issue in 3D plot"

    def test_properties_yaxis_title_3D_plot(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm", "PetalLengthCm"])
        # Assert
        assert (
            result.layout["scene"]["yaxis"]["title"]["text"] == "SepalLengthCm"
        ), "Y-axis title issue in 3D plot"

    def test_properties_zaxis_title_3D_plot(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm", "PetalLengthCm"])
        # Assert
        assert (
            result.layout["scene"]["zaxis"]["title"]["text"] == "PetalLengthCm"
        ), "Z-axis title issue in 3D plot"

    def test_properties_all_unique_values_for_by(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["PetalWidthCm", "PetalLengthCm",], by="Species",)
        # Assert
        assert set(
            [result.data[0]["name"], result.data[1]["name"], result.data[2]["name"]]
        ).issubset(
            set(["Iris-virginica", "Iris-versicolor", "Iris-setosa"])
        ), "Some unique values were not found in the plot"

    def test_properties_all_unique_values_for_by_3D_plot(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(
            ["PetalWidthCm", "PetalLengthCm", "SepalLengthCm"], by="Species"
        )
        # Assert
        assert set(
            [result.data[0]["name"], result.data[1]["name"], result.data[2]["name"]]
        ).issubset(
            set(["Iris-virginica", "Iris-versicolor", "Iris-setosa"])
        ), "Some unique values were not found in the 3D plot"

    def test_properties_colors_for_by(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["PetalWidthCm", "PetalLengthCm",], by="Species",)
        assert (
            len(
                set(
                    [
                        result.data[0]["marker"]["color"],
                        result.data[1]["marker"]["color"],
                        result.data[2]["marker"]["color"],
                    ]
                )
            )
            == 3
        ), "Colors are not unique for three different cat_col parameter"

    def test_properties_colors_for_by_3D_plot(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(
            ["PetalWidthCm", "PetalLengthCm", "SepalLengthCm"], by="Species"
        )
        assert (
            len(
                set(
                    [
                        result.data[0]["marker"]["color"],
                        result.data[1]["marker"]["color"],
                        result.data[2]["marker"]["color"],
                    ]
                )
            )
            == 3
        ), "Colors are not unique for three different cat_col parameter"

    def test_data_total_number_of_points(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm"])
        # Assert - checking if correct object created
        assert len(result.data[0]["x"]) == len(
            iris_vd
        ), "Number of points not consistent with data"
        assert len(result.data[0]["y"]) == len(
            iris_vd
        ), "Number of points not consistent with data"

    def test_data_total_number_of_points_3D_plot(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["PetalWidthCm", "PetalLengthCm", "SepalLengthCm"])
        # Assert - checking if correct object created
        assert len(result.data[0]["x"]) == len(
            iris_vd
        ), "Number of points not consistent with data"
        assert len(result.data[0]["y"]) == len(
            iris_vd
        ), "Number of points not consistent with data"
        assert len(result.data[0]["z"]) == len(
            iris_vd
        ), "Number of points not consistent with data"

    def test_data_random_point_from_plot_in_data(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm"])
        # Assert -
        len_of_data = len(
            iris_vd.search(
                conditions=[
                    f"SepalWidthCm ={result.data[0]['x'][0]} and SepalLengthCm={result.data[0]['y'][0]}"
                ],
                usecols=["SepalWidthCm", "SepalLengthCm"],
            )
        )
        assert len_of_data > 0, "A wrong point was plotted"

    def test_data_random_point_from_data_in_plot(self, load_plotly, iris_vd):
        # Arrange
        sample = iris_vd.sample(n=1)
        x_test = sample["SepalWidthCm"][0]
        y_test = sample["SepalLengthCm"][0]
        # Act
        result = iris_vd.scatter(["SepalWidthCm", "SepalLengthCm"])
        # Assert -
        assert (
            y_test in result.data[0]["y"][np.where(result.data[0]["x"] == x_test)[0]]
        ), "A random sample datapoint was not plotted"


class TestVDFBoxPlot:
    def test_properties_output_type(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_output_type_for_partitioned_data(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary")
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_xaxis_title(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        # Assert
        assert result.layout["xaxis"]["title"]["text"] == "0", "X-axis title issue"

    def test_properties_xaxis_title_for_partitioned_data(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary")
        # Assert
        assert result.layout["xaxis"]["title"]["text"] == "binary", "X-axis title issue"

    def test_properties_yaxis_title(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        # Assert
        assert result.layout["yaxis"]["title"]["text"] is None, "Y-axis title issue"

    def test_properties_yaxis_title_for_partitioned_data(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary")
        # Assert
        assert result.layout["yaxis"]["title"]["text"] == "0", "Y-axis title issue"

    def test_properties_orientation(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        # Assert
        assert result.data[0]["orientation"] == "h", "Orientation is not correct"

    def test_properties_orientation(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary")
        # Assert
        assert result.data[0]["orientation"] == "v", "Orientation is not correct"

    def test_properties_bound_hover_labels(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        name_list = []
        for i in range(len(result.data)):
            name_list.append(result.data[i]["hovertemplate"].split(":")[0])
        test_list = ["Lower", "Median", "Upper"]
        is_subset = all(elem in name_list for elem in test_list)
        # Assert
        assert is_subset, "Hover label error"

    def test_properties_bound_hover_labels_for_partitioned_data(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary")
        name_list = []
        for i in range(len(result.data)):
            name_list.append(result.data[i]["hovertemplate"].split(":")[0])
        # Assert
        assert name_list.count("25.0% ") == 2, "Hover label error"
        assert name_list.count("75.0% ") == 2, "Hover label error"
        assert name_list.count("Lower") == 2, "Hover label error"
        assert name_list.count("Median") == 2, "Hover label error"
        assert name_list.count("Upper") == 2, "Hover label error"

    def test_properties_quartile_labels(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        name_list = []
        for i in range(len(result.data)):
            name_list.append(result.data[i]["hovertemplate"].split("%")[0])
        test_list = ["25.0", "75.0"]
        is_subset = all(elem in name_list for elem in test_list)
        # Assert
        assert is_subset, "Hover label error for quantiles"

    def test_properties_quartile_labels_for_custom_q1(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(q=[0.2, 0.7])
        name_list = []
        for i in range(len(result.data)):
            name_list.append(result.data[i]["hovertemplate"].split("%")[0])
        test_list = ["20.0", "70.0"]
        is_subset = all(elem in name_list for elem in test_list)
        # Assert
        assert is_subset, "Hover label error for quantiles"

    def test_properties_quartile_labels_for_custom_q1_for_partitioned_data(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary", q=[0.2, 0.7])
        name_list = []
        for i in range(len(result.data)):
            name_list.append(result.data[i]["hovertemplate"].split("%")[0])
        # Assert
        assert name_list.count("20.0") == 2, "Hover label error for quantiles"
        assert name_list.count("70.0") == 2, "Hover label error for quantiles"

    def test_properties_lower_hover_box_max_value_is_equal_to_minimum_of_q1(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        # Assert
        assert (
            result.data[1]["base"][0] + result.data[1]["x"][0]
            == result.data[2]["base"][0]
        ), "Hover boxes may overlap"

    def test_properties_lower_hover_box_max_value_is_equal_to_minimum_of_q1_for_partitioned_data(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary")
        # Assert
        assert (
            result.data[4]["base"][0] + result.data[4]["y"][0]
            == result.data[5]["base"][0]
        ), "Hover boxes may overlap"

    def test_properties_q1_hover_box_max_value_is_equal_to_minimum_of_median(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        # Assert
        assert (
            result.data[2]["base"][0] + result.data[2]["x"][0]
            == result.data[3]["base"][0]
        ), "Hover boxes may overlap"

    def test_data_median_value(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        # Assert
        assert result.data[0]["median"][0] == pytest.approx(
            50, 1
        ), "median not computed correctly"

    def test_data_median_value_for_partitioned_data_for_x_is_0(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary")
        # Assert
        assert result.data[0]["median"][0] == pytest.approx(
            50, 1
        ), "median not computed correctly for binary=0"

    def test_data_median_value_for_partitioned_data_for_x_is_0(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot(by="binary")
        # Assert
        assert result.data[1]["median"][0] == pytest.approx(
            50, 1
        ), "median not computed correctly for binary=1"

    def test_data_maximum_point_value(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].boxplot()
        # Assert
        assert dummy_dist_vd.max()["max"][0] == max(
            result.data[0]["x"][0]
        ), "Maximum value not in plot"


class TestVDFHeatMap:
    def test_properties_output_type(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.heatmap(["PetalLengthCm", "SepalLengthCm"])
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_output_type_for_pivot_table(self, load_plotly, titanic_vd):
        # Arrange
        # Act
        result = titanic_vd.pivot_table(["survived", "pclass"])
        # Assert - checking if correct object created
        assert (
            type(result) == plotly.graph_objs._figure.Figure
        ), "wrong object crated for pivot table"

    def test_properties_output_type_for_corr(self, load_plotly, titanic_vd):
        # Arrange
        # Act
        result = titanic_vd.corr(method="spearman")
        # Assert - checking if correct object created
        assert (
            type(result) == plotly.graph_objs._figure.Figure
        ), "wrong object crated for corr() plot"

    def test_properties_xaxis_title(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.heatmap(["PetalLengthCm", "SepalLengthCm"])
        # Assert
        assert (
            result.layout["xaxis"]["title"]["text"] == "PetalLengthCm"
        ), "X-axis title issue"

    def test_properties_yaxis_title(self, load_plotly, iris_vd):
        # Arrange
        # Act
        result = iris_vd.heatmap(["PetalLengthCm", "SepalLengthCm"])
        # Assert
        assert (
            result.layout["yaxis"]["title"]["text"] == "SepalLengthCm"
        ), "Y-axis title issue"

    # ToDo Remove double quotes after the labels are fixed
    def test_properties_yaxis_labels_for_categorical_data(
        self, load_plotly, titanic_vd
    ):
        # Arrange
        expected_labels = (
            '"survived"',
            '"pclass"',
            '"fare"',
            '"parch"',
            '"age"',
            '"sibsp"',
            '"body"',
        )
        # Act
        result = titanic_vd.corr(method="pearson", focus="survived")
        # Assert
        assert result.data[0]["y"] == expected_labels, "Y-axis labels incorrect"

    def test_data_matrix_shape(self, load_plotly, iris_vd):
        # Arrange
        expected_shape = (9, 6)
        # Act
        result = iris_vd.heatmap(["PetalLengthCm", "SepalLengthCm"])
        # Assert
        assert (
            result.data[0]["z"].shape == expected_shape
        ), "Incorrect shape of output matrix"

    def test_data_matrix_shape_for_pivot_table(self, load_plotly, titanic_vd):
        # Arrange
        expected_shape = (3, 2)
        # Act
        result = titanic_vd.pivot_table(["survived", "pclass"])
        # Assert
        assert (
            result.data[0]["z"].shape == expected_shape
        ), "Incorrect shape of output matrix"

    def test_data_x_range(self, load_plotly, iris_vd):
        # Arrange
        upper_bound = iris_vd["PetalLengthCm"].max()
        lower_bound = iris_vd["PetalLengthCm"].min()
        # Act
        result = iris_vd.heatmap(["PetalLengthCm", "SepalLengthCm"])
        x_array = np.array(result.data[0]["x"], dtype=float)
        # Assert
        assert np.all(
            (x_array[1:] >= lower_bound) & (x_array[:-1] <= upper_bound)
        ), "X-axis Values outside of data range"

    def test_data_y_range(self, load_plotly, iris_vd):
        # Arrange
        upper_bound = iris_vd["SepalLengthCm"].max()
        lower_bound = iris_vd["SepalLengthCm"].min()
        # Act
        result = iris_vd.heatmap(["PetalLengthCm", "SepalLengthCm"])
        y_array = np.array(result.data[0]["y"], dtype=float)
        # Assert
        assert np.all(
            (y_array[:-1] >= lower_bound) & (y_array[1:] <= upper_bound)
        ), "X-axis Values outside of data range"

    def test_additional_options_custom_width_height(self, load_plotly, iris_vd):
        # Arrange
        custom_width = 400
        custom_height = 700
        # Act
        result = iris_vd.heatmap(
            ["PetalLengthCm", "SepalLengthCm"], width=custom_width, height=custom_height
        )
        # Assert
        assert (
            result.layout["width"] == custom_width
            and result.layout["height"] == custom_height
        )


class TestVDFLinePlot:
    def test_properties_output_type(self, load_plotly, amazon_vd):
        # Arrange
        amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')")
        # Act
        result = amazon_vd["number"].plot(ts="date", by="state")
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_output_type_for_vDataFrame(self, load_plotly, amazon_vd):
        # Arrange
        # Act
        result = amazon_vd.plot(ts="date", columns=["number"])
        # Assert - checking if correct object created
        assert (
            type(result) == plotly.graph_objs._figure.Figure
        ), "wrong object crated for vDataFrame"

    def test_properties_output_type_for_one_trace(self, load_plotly, amazon_vd):
        # Arrange
        amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')")
        # Act
        result = amazon_vd["number"].plot(ts="date")
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_x_axis_title(self, load_plotly, amazon_vd):
        # Arrange
        amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')")
        # Act
        result = amazon_vd["number"].plot(ts="date", by="state")
        # Assert - checking if correct object created
        assert (
            result.layout["xaxis"]["title"]["text"] == "time"
        ), "X axis title incorrect"

    def test_properties_y_axis_title(self, load_plotly, amazon_vd):
        # Arrange
        amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')")
        # Act
        result = amazon_vd["number"].plot(ts="date", by="state")
        # Assert - checking if correct object created
        assert (
            result.layout["yaxis"]["title"]["text"] == "number"
        ), "Y axis title incorrect"

    def test_data_count_of_all_values(self, load_plotly, amazon_vd):
        # Arrange
        amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')")
        # Act
        result = amazon_vd["number"].plot(ts="date", by="state")
        assert (
            result.data[0]["x"].shape[0] + result.data[1]["x"].shape[0]
            == amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')").shape()[0]
        ), "The total values in the plot are not equal to the values in the dataframe."

    def test_data_spot_check(self, load_plotly, amazon_vd):
        # Arrange
        amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')")
        # Act
        result = amazon_vd["number"].plot(ts="date", by="state")
        assert (
            amazon_vd["date"][random.randint(0, len(amazon_vd))] in result.data[0]["x"]
        ), "One date that exists in the data does not exist in the plot"

    def test_additional_options_custom_width(self, load_plotly, amazon_vd):
        # Arrange
        amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')")
        # Act
        result = amazon_vd["number"].plot(ts="date", by="state", width=400)
        # Assert - checking if correct object created
        assert result.layout["width"] == 400, "Custom width not working"

    def test_additional_options_custom_height(self, load_plotly, amazon_vd):
        # Arrange
        custom_height = 600
        # Act
        result = amazon_vd["number"].plot(ts="date", width=600, height=custom_height)
        # Assert - checking if correct object created
        assert result.layout["height"] == custom_height, "Custom height not working"

    def test_additional_options_marker_on(self, load_plotly, amazon_vd):
        # Arrange
        amazon_vd.filter("state IN ('AMAZONAS', 'BAHIA')")
        # Act
        result = amazon_vd["number"].plot(ts="date", markers=True)
        # Assert - checking if correct object created
        assert set(result.data[0]["mode"]) == set(
            "lines+markers"
        ), "Markers not turned on"


class TestVDFContourPlot:
    def test_properties_output_type(self, load_plotly, dummy_dist_vd):
        # Arrange
        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd.contour(["0", "binary"], func)
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "Wrong object created"

    def test_properties_x_axis_title(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Arrange
        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd.contour(["0", "binary"], func)
        # Assert
        assert result.layout["xaxis"]["title"]["text"] == "0", "X axis title incorrect"

    def test_properties_y_axis_title(self, load_plotly, dummy_dist_vd):
        # Arrange
        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd.contour(["0", "binary"], func)
        # Assert
        assert (
            result.layout["yaxis"]["title"]["text"] == "binary"
        ), "Y axis title incorrect"

    def test_data_count_xaxis_default_bins(self, load_plotly, dummy_dist_vd):
        # Arrange
        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd.contour(["0", "binary"], func)
        # Assert
        assert result.data[0]["x"].shape[0] == 100, "The default bins are not 100."

    def test_data_count_xaxis_custom_bins(self, load_plotly, dummy_dist_vd):
        # Arrange
        custom_bins = 1000

        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd.contour(
            columns=["0", "binary"], nbins=custom_bins, func=func
        )
        # Assert
        assert (
            result.data[0]["x"].shape[0] == custom_bins
        ), "The custom bins option is not working."

    def test_data_x_axis_range(self, load_plotly, dummy_dist_vd):
        # Arrange
        x_min = dummy_dist_vd["0"].min()
        x_max = dummy_dist_vd["0"].max()
        custom_bins = 1000

        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd.contour(columns=["0", "binary"], func=func)
        assert (
            result.data[0]["x"].min() == x_min and result.data[0]["x"].max() == x_max
        ), "The range in data is not consistent with plot"

    def test_additional_options_custom_width(self, load_plotly, dummy_dist_vd):
        # Arrange
        custom_width = 700

        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd.contour(["0", "binary"], func, width=custom_width)
        # Assert
        assert result.layout["width"] == custom_width, "Custom width not working"

    def test_additional_options_custom_height(self, load_plotly, dummy_dist_vd):
        #
        custom_height = 700

        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd.contour(["0", "binary"], func, height=custom_height)
        # Assert
        assert result.layout["height"] == custom_height, "Custom height not working"


class TestVDFDensityPlot:
    def test_properties_output_type(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].density()
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_output_type_for_multiplot(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].density(by="binary")
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    # ToDO - Change below after quotation bug fixed
    def test_properties_x_axis_title(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].density()
        # Assert -
        assert (
            result.layout["xaxis"]["title"]["text"] == '"0"'
        ), "X axis title incorrect"

    def test_properties_y_axis_title(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["0"].density()
        # Assert
        assert (
            result.layout["yaxis"]["title"]["text"] == "density"
        ), "Y axis title incorrect"

    def test_properties_multiple_plots_produced_for_multiplot(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        number_of_plots = 2
        # Act
        result = dummy_dist_vd["0"].density(by="binary")
        # Assert
        assert (
            len(result.data) == number_of_plots
        ), "Two plots not produced for two classes"

    def test_data_x_axis_range(self, load_plotly, dummy_dist_vd):
        # Arrange
        x_min = dummy_dist_vd["0"].min()
        x_max = dummy_dist_vd["0"].max()

        def func(a, b):
            return b

        # Act
        result = dummy_dist_vd["0"].density()
        assert pytest.approx(result.data[0]["x"].min(), 4) == pytest.approx(
            x_min, 4
        ) and pytest.approx(result.data[0]["x"].max(), 4) == pytest.approx(
            x_max, 4
        ), "The range in data is not consistent with plot"

    def test_additional_options_custom_width(self, load_plotly, dummy_dist_vd):
        # Arrange
        custom_width = 700
        # Act
        result = dummy_dist_vd["0"].density(width=custom_width)
        # Assert
        assert result.layout["width"] == custom_width, "Custom width not working"

    def test_additional_options_custom_height(self, load_plotly, dummy_dist_vd):
        # rrange
        custom_height = 700
        # Act
        result = dummy_dist_vd["0"].density(height=custom_height)
        # Assert
        assert result.layout["height"] == custom_height, "Custom height not working"


class TestVDFSpiderPlot:
    def test_properties_output_type(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["cats"].spider()
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_output_type_for_multiplot(self, load_plotly, dummy_dist_vd):
        # Arrange
        # Act
        result = dummy_dist_vd["cats"].spider(by="binary")
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_title(self, load_plotly, dummy_dist_vd):
        # Arrange
        column_name = "cats"
        # Act
        result = dummy_dist_vd[column_name].spider()
        # Assert -
        assert result.layout["title"]["text"] == column_name, "Title incorrect"

    def test_properties_method_title_at_bottom(self, load_plotly, dummy_dist_vd):
        # Arrange
        method_text = "(Method: Density)"
        # Act
        result = dummy_dist_vd["cats"].spider()
        # Assert -
        assert (
            result.layout["annotations"][0]["text"] == method_text
        ), "Method title incorrect"

    def test_properties_multiple_plots_produced_for_multiplot(
        self, load_plotly, dummy_dist_vd
    ):
        # Arrange
        number_of_plots = 2
        # Act
        result = dummy_dist_vd["cats"].spider(by="binary")
        # Assert
        assert (
            len(result.data) == number_of_plots
        ), "Two traces not produced for two classes of binary"

    def test_data_all_categories(self, load_plotly, dummy_dist_vd):
        # Arrange
        no_of_category = dummy_dist_vd["cats"].nunique()
        # Act
        result = dummy_dist_vd["cats"].spider()
        assert (
            result.data[0]["r"].shape[0] == no_of_category
        ), "The number of categories in the data differ from the plot"

    def test_additional_options_custom_width(self, load_plotly, dummy_dist_vd):
        # Arrange
        custom_width = 700
        # Act
        result = dummy_dist_vd["cats"].spider(width=custom_width)
        # Assert
        assert result.layout["width"] == custom_width, "Custom width not working"

    def test_additional_options_custom_height(self, load_plotly, dummy_dist_vd):
        # rrange
        custom_height = 700
        # Act
        result = dummy_dist_vd["cats"].spider(height=custom_height)
        # Assert
        assert result.layout["height"] == custom_height, "Custom height not working"


class TestVDFRangeCurve:
    def test_properties_output_type(self, load_plotly, dummy_date_vd):
        # Arrange
        # Act
        result = dummy_date_vd["value"].range_plot(ts="date", plot_median=True)
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_xaxis(self, load_plotly, dummy_date_vd):
        # Arrange
        column_name = "date"
        # Act
        result = dummy_date_vd["value"].range_plot(ts=column_name, plot_median=True)
        # Assert -
        assert (
            result.layout["xaxis"]["title"]["text"] == column_name
        ), "X axis label incorrect"

    def test_properties_xaxis(self, load_plotly, dummy_date_vd):
        # Arrange
        column_name = "value"
        # Act
        result = dummy_date_vd[column_name].range_plot(ts="date", plot_median=True)
        # Assert -
        assert (
            result.layout["yaxis"]["title"]["text"] == column_name
        ), "Y axis label incorrect"

    def test_data_x_axis(self, load_plotly, dummy_date_vd):
        # Arrange
        test_set = set([1910, 1920, 1930, 1940, 1950])
        # Act
        result = dummy_date_vd["value"].range_plot(ts="date")
        assert set(result.data[0]["x"]).issubset(
            test_set
        ), "There is descripancy between x axis values for the bounds"

    def test_data_x_axis_for_median(self, load_plotly, dummy_date_vd):
        # Arrange
        test_set = set([1910, 1920, 1930, 1940, 1950])
        # Act
        result = dummy_date_vd["value"].range_plot(ts="date", plot_median=True)
        assert set(result.data[1]["x"]).issubset(
            test_set
        ), "There is descripancy between x axis values for the median"

    def test_additional_options_turn_off_median(self, load_plotly, dummy_date_vd):
        # Arrange
        # Act
        result = dummy_date_vd["value"].range_plot(ts="date", plot_median=False)
        # Assert
        assert (
            len(result.data) == 1
        ), "Median is still showing even after it is turned off"

    def test_additional_options_turn_on_median(self, load_plotly, dummy_date_vd):
        # Arrange
        # Act
        result = dummy_date_vd["value"].range_plot(ts="date", plot_median=True)
        # Assert
        assert (
            len(result.data) > 1
        ), "Median is still showing even after it is turned off"

    def test_additional_options_custom_width(self, load_plotly, dummy_date_vd):
        # Arrange
        custom_width = 700
        # Act
        result = dummy_date_vd["value"].range_plot(ts="date", width=custom_width)
        # Assert
        assert result.layout["width"] == custom_width, "Custom width not working"

    def test_additional_options_custom_height(self, load_plotly, dummy_date_vd):
        # rrange
        custom_height = 700
        # Act
        result = dummy_date_vd["value"].range_plot(ts="date", height=custom_height)
        # Assert
        assert result.layout["height"] == custom_height, "Custom height not working"


class TestVDFOutliersPlot:
    def test_properties_output_type_for_1d(self, load_plotly, titanic_vd):
        # Arrange
        # Act
        result = titanic_vd.outliers_plot(columns=["age"])
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_output_type_for_2d(self, load_plotly, titanic_vd):
        # Arrange
        # Act
        result = titanic_vd.outliers_plot(columns=["age", "fare"])
        # Assert - checking if correct object created
        assert type(result) == plotly.graph_objs._figure.Figure, "wrong object crated"

    def test_properties_xaxis_for_1d(self, load_plotly, titanic_vd):
        # Arrange
        column_name = "age"
        # Act
        result = titanic_vd.outliers_plot(columns=[column_name])
        # Assert -
        assert result.data[1]["x"][0] == column_name, "X axis label incorrect"

    def test_properties_xaxis_for_2d(self, load_plotly, titanic_vd):
        # Arrange
        column_name = "age"
        # Act
        result = titanic_vd.outliers_plot(columns=[column_name, "fare"])
        # Assert -
        assert (
            result.layout["xaxis"]["title"]["text"] == column_name
        ), "X axis label incorrect"

    def test_properties_yaxis_for_2d(self, load_plotly, titanic_vd):
        # Arrange
        column_name = "fare"
        # Act
        result = titanic_vd.outliers_plot(columns=["age", column_name])
        # Assert -
        assert (
            result.layout["yaxis"]["title"]["text"] == column_name
        ), "X axis label incorrect"

    def test_data_all_scatter_points_for_1d(self, load_plotly, titanic_vd):
        # Arrange
        total_points = len(titanic_vd["age"])
        # Act
        result = titanic_vd.outliers_plot(columns=["age"], max_nb_points=10000)
        assert (
            result.data[0]["y"].shape[0] + result.data[1]["y"].shape[0] == total_points
        ), "All points are not plotted for 1d plot"

    def test_data_all_scatter_points_for_2d(self, load_plotly, titanic_vd):
        # Arrange
        total_points = len(titanic_vd["age"])
        # Act
        result = titanic_vd.outliers_plot(columns=["age", "fare"], max_nb_points=10000)
        assert result.data[-1]["y"].shape[0] + result.data[-2]["y"].shape[
            0
        ] == pytest.approx(
            total_points, abs=1
        ), "All points are not plotted for 2d plot"

    def test_data_all_sinformation_plotted_for_2d(self, load_plotly, titanic_vd):
        # Arrange
        total_elements = 4
        # Act
        result = titanic_vd.outliers_plot(columns=["age", "fare"])
        assert (
            len(result.data) == total_elements
        ), "The total number of elements plotted is not correct"

    def test_additional_options_custom_width(self, load_plotly, titanic_vd):
        # Arrange
        custom_width = 700
        # Act
        result = titanic_vd.outliers_plot(columns=["age", "fare"], width=custom_width)
        # Assert
        assert result.layout["width"] == custom_width, "Custom width not working"

    def test_additional_options_custom_height(self, load_plotly, titanic_vd):
        # rrange
        custom_height = 700
        # Act
        result = titanic_vd.outliers_plot(columns=["age", "fare"], height=custom_height)
        # Assert
        assert result.layout["height"] == custom_height, "Custom height not working"


class TestVDFACFPlot:
    def test_properties_output_type_for(self, acf_plot_result):
        # Arrange
        # Act
        # Assert - checking if correct object created
        assert (
            type(acf_plot_result) == plotly.graph_objs._figure.Figure
        ), "wrong object crated"

    def test_properties_xaxis_label(self, acf_plot_result):
        # Arrange
        test_title = "Lag"
        # Act
        # Assert - checking if correct object created
        assert (
            acf_plot_result.layout["xaxis"]["title"]["text"] == test_title
        ), "X axis label incorrect"

    def test_properties_scatter_points_and_confidence(self, acf_plot_result):
        # Arrange
        total_elements = 3
        # Act
        # Assert - checking if correct object created
        assert (
            len(acf_plot_result.data) == total_elements
        ), "Some elements of plot are missing"

    def test_properties_vertical_lines_for_custom_lag(self, load_plotly, amazon_vd):
        # Arrange
        lag_number = 24
        # Act
        result = amazon_vd.acf(
            ts="date",
            column="number",
            p=lag_number - 1,
            by=["state"],
            unit="month",
            method="spearman",
        )
        # Assert - checking if correct object created
        assert (
            len(result.layout["shapes"]) == lag_number
        ), "Number of vertical lines inconsistent"

    def test_properties_mode_lines(self, load_plotly, amazon_vd):
        # Arrange
        mode = "lines+markers"
        # Act
        result = amazon_vd.acf(
            ts="date",
            column="number",
            p=12,
            by=["state"],
            unit="month",
            method="spearman",
            kind="line",
        )
        # Assert - checking if correct object created
        assert result.data[-1]["mode"] == mode, "Number of vertical lines inconsistent"

    def test_data_all_scatter_points(self, acf_plot_result):
        # Arrange
        lag_number = 13
        # Act
        # Assert - checking if correct object created
        assert (
            len(acf_plot_result.data[0]["x"]) == lag_number
        ), "Number of lag points inconsistent"

    def test_additional_options_custom_width(self, load_plotly, amazon_vd):
        # Arrange
        custom_width = 700
        # Act
        result = amazon_vd.acf(
            ts="date",
            column="number",
            p=12,
            by=["state"],
            unit="month",
            method="spearman",
            width=custom_width,
        )
        # Assert - checking if correct object created
        assert result.layout["width"] == custom_width, "Custom width not working"

    def test_additional_options_custom_height(self, load_plotly, amazon_vd):
        # rrange
        custom_height = 700
        # Act
        result = amazon_vd.acf(
            ts="date",
            column="number",
            p=12,
            by=["state"],
            unit="month",
            method="spearman",
            height=custom_height,
        )
        # Assert - checking if correct object created
        assert result.layout["height"] == custom_height, "Custom height not working"


class TestMachineLearningElbowCurve:
    def test_properties_output_type_for(self, elbow_plot_result):
        # Arrange
        # Act
        # Assert - checking if correct object created
        assert (
            type(elbow_plot_result) == plotly.graph_objs._figure.Figure
        ), "wrong object crated"

    def test_properties_xaxis_label(self, elbow_plot_result):
        # Arrange
        test_title = "Number of Clusters"
        # Act
        # Assert - checking if correct object created
        assert (
            elbow_plot_result.layout["xaxis"]["title"]["text"] == test_title
        ), "X axis label incorrect"

    def test_data_all_scatter_points(self, elbow_plot_result):
        # Arrange
        mode = "markers+line"
        # Act
        # Assert - checking if correct object created
        assert set(elbow_plot_result.data[0]["mode"]) == set(
            mode
        ), "Either lines or marker missing"

    def test_additional_options_custom_height(self, load_plotly, iris_vd):
        # rrange
        custom_height = 650
        custom_width = 700
        # Act
        result = elbow(
            input_relation=iris_vd,
            X=["PetalLengthCm", "PetalWidthCm"],
            width=custom_width,
            height=custom_height,
        )
        # Assert - checking if correct object created
        assert (
            result.layout["height"] == custom_height
            and result.layout["width"] == custom_width
        ), "Custom height and width not working"


class TestMachineLearningRegressionPlot:
    def test_properties_output_type_for(self, regression_plot_result):
        # Arrange
        # Act
        # Assert - checking if correct object created
        assert (
            type(regression_plot_result) == plotly.graph_objs._figure.Figure
        ), "wrong object crated"

    def test_properties_xaxis_label(self, regression_plot_result):
        # Arrange
        test_title = "x"
        # Act
        # Assert
        assert (
            regression_plot_result.layout["xaxis"]["title"]["text"] == test_title
        ), "X axis label incorrect"

    def test_properties_yaxis_label(self, regression_plot_result):
        # Arrange
        test_title = "y"
        # Act
        # Assert
        assert (
            regression_plot_result.layout["yaxis"]["title"]["text"] == test_title
        ), "Y axis label incorrect"

    def test_properties_scatter_and_line_plot(self, regression_plot_result):
        # Arrange
        total_items = 2
        # Act
        # Assert
        assert (
            len(regression_plot_result.data) == total_items
        ), "Either line or scatter missing"

    def test_data_all_scatter_points(self, regression_plot_result):
        # Arrange
        no_of_points = 100
        # Act
        # Assert
        assert (
            len(regression_plot_result.data[0]["x"]) == no_of_points
        ), "Discrepancy between points plotted and total number ofp oints"

    def test_additional_options_custom_height(self, load_plotly, dummy_scatter_vd):
        # rrange
        custom_height = 650
        custom_width = 700
        # Act
        model = LinearRegression("LR_churn")
        model.fit(dummy_scatter_vd, ["x"], "y")
        result = model.plot(height=custom_height, width=custom_width)
        # Assert
        assert (
            result.layout["height"] == custom_height
            and result.layout["width"] == custom_width
        ), "Custom height and width not working"
