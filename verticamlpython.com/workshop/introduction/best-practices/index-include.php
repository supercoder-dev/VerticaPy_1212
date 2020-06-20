<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="Best-Practices">Best Practices<a class="anchor-link" href="#Best-Practices">&#182;</a></h1>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>As all API or software, Vertica ML Python has a cost. The user needs to understand Vertica and Vertica ML Python architectures to be really performant. We will go through the different ways to optimize the process.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="1.-Optimize-your-architecture-at-the-DataBase-level">1. Optimize your architecture at the DataBase level<a class="anchor-link" href="#1.-Optimize-your-architecture-at-the-DataBase-level">&#182;</a></h1>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>Do not forget that Vertica ML Python is an abstraction of SQL. Everything which will optimize Vertica performance will make Vertica ML Python more performant. The SQL code generation is automatic and there is nothing you can optimize from this side except following the next best practices. However most of the optimization resides on the Projections. Think in advance about your data architecture before creating a vDataFrame to select only the needed columns. In the following example, we use the 'usecols' parameter of the vDataFrame to only select the needed columns.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[12]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">from</span> <span class="nn">vertica_ml_python</span> <span class="k">import</span> <span class="o">*</span>
<span class="n">vdf</span> <span class="o">=</span> <span class="n">vDataFrame</span><span class="p">(</span><span class="s2">&quot;public.titanic&quot;</span><span class="p">,</span>
                 <span class="n">usecols</span> <span class="o">=</span> <span class="p">[</span><span class="s2">&quot;survived&quot;</span><span class="p">,</span> <span class="s2">&quot;pclass&quot;</span><span class="p">,</span> <span class="s2">&quot;age&quot;</span><span class="p">])</span>
<span class="nb">print</span><span class="p">(</span><span class="n">vdf</span><span class="p">)</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<table style="border-collapse: collapse; border: 2px solid white"><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b></b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>pclass</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>age</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>survived</b></td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>0</b></td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">2.0</td><td style="border: 1px solid white;">0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>1</b></td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">30.0</td><td style="border: 1px solid white;">0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>2</b></td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">25.0</td><td style="border: 1px solid white;">0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>3</b></td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">39.0</td><td style="border: 1px solid white;">0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>4</b></td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">71.0</td><td style="border: 1px solid white;">0</td></tr><tr><td style="border-top: 1px solid white;background-color:#263133;color:white"></td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td></tr></table>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&lt;object&gt;  Name: titanic, Number of rows: 1234, Number of columns: 3
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="2.-Save-the-current-relation-when-you-can">2. Save the current relation when you can<a class="anchor-link" href="#2.-Save-the-current-relation-when-you-can">&#182;</a></h1>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>vDataFrame works the same way a view is. If the final generated relation uses a lot of different functions, it will drastically increase the computation time needed at each method call.</p>
<p>When the transformations are light they will not slow down the process whereas when the transformations are heavy (multiple joins, abusive usage of advanced analytical funcions or moving windows), it is highly advised to save the vDataFrame structure. Let's look at an example.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[4]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># Doing multiple operation</span>
<span class="n">vdf</span><span class="p">[</span><span class="s2">&quot;sex&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">label_encode</span><span class="p">()[</span><span class="s2">&quot;boat&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">fillna</span><span class="p">(</span><span class="n">method</span> <span class="o">=</span> <span class="s2">&quot;0ifnull&quot;</span><span class="p">)[</span><span class="s2">&quot;name&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">str_extract</span><span class="p">(</span>
    <span class="s1">&#39; ([A-Za-z]+)\.&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">eval</span><span class="p">(</span><span class="s2">&quot;family_size&quot;</span><span class="p">,</span> <span class="n">expr</span> <span class="o">=</span> <span class="s2">&quot;parch + sibsp + 1&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span>
    <span class="n">columns</span> <span class="o">=</span> <span class="p">[</span><span class="s2">&quot;cabin&quot;</span><span class="p">,</span> <span class="s2">&quot;body&quot;</span><span class="p">,</span> <span class="s2">&quot;ticket&quot;</span><span class="p">,</span> <span class="s2">&quot;home.dest&quot;</span><span class="p">])[</span><span class="s2">&quot;fare&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">fill_outliers</span><span class="p">()</span><span class="o">.</span><span class="n">fillna</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="n">vdf</span><span class="o">.</span><span class="n">current_relation</span><span class="p">())</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>795 element(s) was/were filled
(
   SELECT
     &#34;survived&#34;,
     &#34;boat&#34;,
     &#34;embarked&#34;,
     &#34;sibsp&#34;,
     COALESCE(&#34;fare&#34;, 32.9113074018842) AS &#34;fare&#34;,
     &#34;sex&#34;,
     &#34;pclass&#34;,
     &#34;age&#34;,
     &#34;name&#34;,
     &#34;parch&#34;,
     &#34;family_size&#34; 
   FROM
 (
   SELECT
     &#34;survived&#34;,
     DECODE(&#34;boat&#34;, NULL, 0, 1) AS &#34;boat&#34;,
     COALESCE(&#34;embarked&#34;, &#39;S&#39;) AS &#34;embarked&#34;,
     &#34;sibsp&#34;,
     (CASE WHEN &#34;fare&#34; &lt; -176.6204982585513 THEN -176.6204982585513 WHEN &#34;fare&#34; &gt; 244.5480856064831 THEN 244.5480856064831 ELSE &#34;fare&#34; END) AS &#34;fare&#34;,
     DECODE(&#34;sex&#34;, &#39;female&#39;, 0, &#39;male&#39;, 1, 2) AS &#34;sex&#34;,
     &#34;pclass&#34;,
     COALESCE(&#34;age&#34;, 30.1524573721163) AS &#34;age&#34;,
     REGEXP_SUBSTR(&#34;name&#34;, &#39; ([A-Za-z]+)\.&#39;) AS &#34;name&#34;,
     &#34;parch&#34;,
     parch + sibsp + 1 AS &#34;family_size&#34; 
   FROM
 (
   SELECT
     &#34;survived&#34;,
     &#34;boat&#34;,
     &#34;embarked&#34;,
     &#34;sibsp&#34;,
     &#34;fare&#34;,
     &#34;sex&#34;,
     &#34;pclass&#34;,
     &#34;age&#34;,
     &#34;name&#34;,
     &#34;parch&#34; 
   FROM
 &#34;public&#34;.&#34;titanic&#34;) 
VERTICA_ML_PYTHON_SUBTABLE) 
VERTICA_ML_PYTHON_SUBTABLE) 
VERTICA_ML_PYTHON_SUBTABLE
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>We can look at the explain plan of the new relation. It can help us to understand how Vertica will work when executing the different aggregations.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[5]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="nb">print</span><span class="p">(</span><span class="n">vdf</span><span class="o">.</span><span class="n">explain</span><span class="p">())</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>------------------------------ 
QUERY PLAN DESCRIPTION: 

EXPLAIN SELECT * FROM (SELECT &#34;survived&#34;, &#34;boat&#34;, &#34;embarked&#34;, &#34;sibsp&#34;, COALESCE(&#34;fare&#34;, 32.9113074018842) AS &#34;fare&#34;, &#34;sex&#34;, &#34;pclass&#34;, &#34;age&#34;, &#34;name&#34;, &#34;parch&#34;, &#34;family_size&#34; FROM (SELECT &#34;survived&#34;, DECODE(&#34;boat&#34;, NULL, 0, 1) AS &#34;boat&#34;, COALESCE(&#34;embarked&#34;, &#39;S&#39;) AS &#34;embarked&#34;, &#34;sibsp&#34;, (CASE WHEN &#34;fare&#34; &lt; -176.6204982585513 THEN -176.6204982585513 WHEN &#34;fare&#34; &gt; 244.5480856064831 THEN 244.5480856064831 ELSE &#34;fare&#34; END) AS &#34;fare&#34;, DECODE(&#34;sex&#34;, &#39;female&#39;, 0, &#39;male&#39;, 1, 2) AS &#34;sex&#34;, &#34;pclass&#34;, COALESCE(&#34;age&#34;, 30.1524573721163) AS &#34;age&#34;, REGEXP_SUBSTR(&#34;name&#34;, &#39; ([A-Za-z]+)\.&#39;) AS &#34;name&#34;, &#34;parch&#34;, parch + sibsp + 1 AS &#34;family_size&#34; FROM (SELECT &#34;survived&#34;, &#34;boat&#34;, &#34;embarked&#34;, &#34;sibsp&#34;, &#34;fare&#34;, &#34;sex&#34;, &#34;pclass&#34;, &#34;age&#34;, &#34;name&#34;, &#34;parch&#34; FROM &#34;public&#34;.&#34;titanic&#34;) VERTICA_ML_PYTHON_SUBTABLE) VERTICA_ML_PYTHON_SUBTABLE) VERTICA_ML_PYTHON_SUBTABLE

Access Path:
+-STORAGE ACCESS for titanic [Cost: 67, Rows: 1K (NO STATISTICS)] (PATH ID: 1)
|  Projection: public.titanic_super
|  Materialize: titanic.pclass, titanic.survived, titanic.name, titanic.sex, titanic.age, titanic.sibsp, titanic.parch, titanic.fare, titanic.embarked, titanic.boat


----------------------------------------------- 
PLAN: BASE QUERY PLAN (GraphViz Format)
----------------------------------------------- 
digraph G {
graph [rankdir=BT, label = &#34;BASE QUERY PLAN
	Query: EXPLAIN SELECT * FROM (SELECT \&#34;survived\&#34;, \&#34;boat\&#34;, \&#34;embarked\&#34;, \&#34;sibsp\&#34;, COALESCE(\&#34;fare\&#34;, 32.9113074018842) AS \&#34;fare\&#34;, \&#34;sex\&#34;, \&#34;pclass\&#34;, \&#34;age\&#34;, \&#34;name\&#34;, \&#34;parch\&#34;, \&#34;family_size\&#34; FROM (SELECT \&#34;survived\&#34;, DECODE(\&#34;boat\&#34;, NULL, 0, 1) AS \&#34;boat\&#34;, COALESCE(\&#34;embarked\&#34;, \&#39;S\&#39;) AS \&#34;embarked\&#34;, \&#34;sibsp\&#34;, (CASE WHEN \&#34;fare\&#34; \&lt; -176.6204982585513 THEN -176.6204982585513 WHEN \&#34;fare\&#34; \&gt; 244.5480856064831 THEN 244.5480856064831 ELSE \&#34;fare\&#34; END) AS \&#34;fare\&#34;, DECODE(\&#34;sex\&#34;, \&#39;female\&#39;, 0, \&#39;male\&#39;, 1, 2) AS \&#34;sex\&#34;, \&#34;pclass\&#34;, COALESCE(\&#34;age\&#34;, 30.1524573721163) AS \&#34;age\&#34;, REGEXP_SUBSTR(\&#34;name\&#34;, \&#39; ([A-Za-z]+)\.\&#39;) AS \&#34;name\&#34;, \&#34;parch\&#34;, parch + sibsp + 1 AS \&#34;family_size\&#34; FROM (SELECT \&#34;survived\&#34;, \&#34;boat\&#34;, \&#34;embarked\&#34;, \&#34;sibsp\&#34;, \&#34;fare\&#34;, \&#34;sex\&#34;, \&#34;pclass\&#34;, \&#34;age\&#34;, \&#34;name\&#34;, \&#34;parch\&#34; FROM \&#34;public\&#34;.\&#34;titanic\&#34;) VERTICA_ML_PYTHON_SUBTABLE) VERTICA_ML_PYTHON_SUBTABLE) VERTICA_ML_PYTHON_SUBTABLE
	
	All Nodes Vector: 
	
	  node[0]=v_testdb_node0001 (initiator) Up
	&#34;, labelloc=t, labeljust=l ordering=out]
0[label = &#34;Root 
	OutBlk=[UncTuple(11)]&#34;, color = &#34;green&#34;, shape = &#34;house&#34;];
1[label = &#34;NewEENode 
	OutBlk=[UncTuple(11)]&#34;, color = &#34;green&#34;, shape = &#34;box&#34;];
2[label = &#34;StorageUnionStep: titanic_super
	Unc: Integer(8)
	Unc: Integer(8)
	Unc: Varchar(20)
	Unc: Integer(8)
	Unc: Numeric(18, 13)
	Unc: Integer(8)
	Unc: Integer(8)
	Unc: Numeric(16, 13)
	Unc: Varchar(164)
	Unc: Integer(8)
	Unc: Integer(8)&#34;, color = &#34;purple&#34;, shape = &#34;box&#34;];
3[label = &#34;ExprEval: 
	  titanic.survived
	  CASE titanic.boat WHEN NULLSEQUAL NULL THEN 0 ELSE 1 END
	  coalesce(titanic.embarked, \&#39;S\&#39;)
	  titanic.sibsp
	  coalesce(CASE WHEN (titanic.fare \&lt; (-176.6204982585513)) THEN (-176.6204982585513) WHEN (titanic.fare \&gt; 244.5480856064831) THEN 244.5480856064831 ELSE titanic.fare END, 32.9113074018842)
	  CASE titanic.sex WHEN NULLSEQUAL \&#39;female\&#39; THEN 0 WHEN NULLSEQUAL \&#39;male\&#39; THEN 1 ELSE 2 END
	  titanic.pclass
	  coalesce(titanic.age, 30.1524573721163)
	  regexp_substr(titanic.name, E\&#39; ([A-Za-z]+)\\.\&#39;, 1, 1, \&#39;\&#39;, 0)
	  titanic.parch
	  ((titanic.parch + titanic.sibsp) + 1)
	Unc: Integer(8)
	Unc: Integer(8)
	Unc: Varchar(20)
	Unc: Integer(8)
	Unc: Numeric(18, 13)
	Unc: Integer(8)
	Unc: Integer(8)
	Unc: Numeric(16, 13)
	Unc: Varchar(164)
	Unc: Integer(8)
	Unc: Integer(8)&#34;, color = &#34;brown&#34;, shape = &#34;box&#34;];
4[label = &#34;ScanStep: titanic_super
	pclass
	survived
	name
	sex
	age
	sibsp
	parch
	fare
	embarked
	boat
	Unc: Integer(8)
	Unc: Integer(8)
	Unc: Varchar(164)
	Unc: Varchar(20)
	Unc: Numeric(6, 3)
	Unc: Integer(8)
	Unc: Integer(8)
	Unc: Numeric(10, 5)
	Unc: Varchar(20)
	Unc: Varchar(100)&#34;, color = &#34;brown&#34;, shape = &#34;box&#34;];
1-&gt;0 [label = &#34;V[0] C=11&#34;, color = &#34;black&#34;, style=&#34;bold&#34;, arrowtail=&#34;inv&#34;];
2-&gt;1 [label = &#34;0&#34;, color = &#34;blue&#34;];
3-&gt;2 [label = &#34;0&#34;, color = &#34;blue&#34;];
4-&gt;3 [label = &#34;0&#34;, color = &#34;blue&#34;];}
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>We did plenty of operations and we must keep in mind that for each method call, this relation will be used to do the different computations. We can save the result as a table in the Vertica DataBase and use the parameter 'inplace' to change the current relation of the vDataFrame by the new one.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[61]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">drop_table</span><span class="p">(</span><span class="s2">&quot;public.titanic_clean&quot;</span><span class="p">)</span>
<span class="n">vdf</span><span class="o">.</span><span class="n">to_db</span><span class="p">(</span><span class="s2">&quot;public.titanic_clean&quot;</span><span class="p">,</span>
              <span class="n">relation_type</span> <span class="o">=</span> <span class="s2">&quot;table&quot;</span><span class="p">,</span>
              <span class="n">inplace</span> <span class="o">=</span> <span class="kc">True</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">vdf</span><span class="o">.</span><span class="n">current_relation</span><span class="p">())</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>The table public.titanic_clean was successfully dropped.
&#34;public&#34;.&#34;titanic_clean&#34;
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>It is obvious that when we are dealing with huge volume of data, we must think twice before saving some transformations. That's why it is preferable to do an entire data exploration first and then do all the transformations when it is really needed.</p>
<h1 id="3.-Use-only-the-important-columns">3. Use only the important columns<a class="anchor-link" href="#3.-Use-only-the-important-columns">&#182;</a></h1>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>Vertica is a columnar MPP DataBase. That's why it is important to understand that most of the optimizations are made in the projections side. Vertica ML Python is not managing this part and it is important that the data you are exploring are well organized when dealing with huge volumes of data. Columnar DataBases are querying faster when less columns are used.</p>
<p>Most of the vDataFrame methods will automatically pick up all the numerical columns even if you have hundreds of them. That's why it is important to look at the functions parameters to pick up only what is needed. Let's look at an example.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[82]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span><span class="o">.</span><span class="n">sql_on_off</span><span class="p">()</span>
<span class="n">vdf</span><span class="o">.</span><span class="n">avg</span><span class="p">()</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<h4 style = 'color : #444444; text-decoration : underline;'>Computes the different aggregations.</h4>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
 &emsp;  SELECT <br> &emsp;  &emsp;  AVG("fare"), <br> &emsp;  &emsp;  AVG("body"), <br> &emsp;  &emsp;  AVG("pclass"), <br> &emsp;  &emsp;  AVG("age"), <br> &emsp;  &emsp;  AVG("parch"), <br> &emsp;  &emsp;  AVG("survived"), <br> &emsp;  &emsp;  AVG("sibsp") &emsp; <br> &emsp;  FROM <br> "public"."titanic" LIMIT 1
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<div style = 'border : 1px dashed black; width : 100%'></div>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<table style="border-collapse: collapse; border: 2px solid white"><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b></b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>avg</b></td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"fare"</b></td><td style="border: 1px solid white;">33.9637936739659</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"body"</b></td><td style="border: 1px solid white;">164.14406779661</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"pclass"</b></td><td style="border: 1px solid white;">2.28444084278768</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"age"</b></td><td style="border: 1px solid white;">30.1524573721163</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"parch"</b></td><td style="border: 1px solid white;">0.378444084278768</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"survived"</b></td><td style="border: 1px solid white;">0.364667747163695</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"sibsp"</b></td><td style="border: 1px solid white;">0.504051863857374</td></tr></table>
</div>

</div>

<div class="output_area">

<div class="prompt output_prompt">Out[82]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>&lt;object&gt;</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>As we did not use the parameter 'columns' to only focus the computation on what is needed, we computed the average of all the numerical columns of the vDataFrame.</p>
<p>When dealing with small volume of data (less than Tb), it is not really important to care about it whereas when the volume is huge the performance will really depend on your data architecture. It is advised to pick up only the needed columns.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[64]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span><span class="o">.</span><span class="n">avg</span><span class="p">(</span><span class="n">columns</span> <span class="o">=</span> <span class="p">[</span><span class="s2">&quot;age&quot;</span><span class="p">,</span> <span class="s2">&quot;survived&quot;</span><span class="p">])</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<h4 style = 'color : #444444; text-decoration : underline;'>Computes the different aggregations.</h4>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
 &emsp;  SELECT <br> &emsp;  &emsp;  AVG("age"), <br> &emsp;  &emsp;  AVG("survived") &emsp; <br> &emsp;  FROM <br> "public"."titanic" LIMIT 1
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<div style = 'border : 1px dashed black; width : 100%'></div>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<table style="border-collapse: collapse; border: 2px solid white"><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b></b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>avg</b></td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"age"</b></td><td style="border: 1px solid white;">30.1524573721163</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"survived"</b></td><td style="border: 1px solid white;">0.364667747163695</td></tr></table>
</div>

</div>

<div class="output_area">

<div class="prompt output_prompt">Out[64]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>&lt;object&gt;</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>If you just need to exclude some columns and to avoid writing all the needed columns name. It is possible to get a list of all the columns without specific ones using the 'get_columns' method.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[83]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">titanic</span><span class="o">.</span><span class="n">get_columns</span><span class="p">()</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt output_prompt">Out[83]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>[&#39;&#34;fare&#34;&#39;,
 &#39;&#34;sex&#34;&#39;,
 &#39;&#34;body&#34;&#39;,
 &#39;&#34;pclass&#34;&#39;,
 &#39;&#34;age&#34;&#39;,
 &#39;&#34;name&#34;&#39;,
 &#39;&#34;cabin&#34;&#39;,
 &#39;&#34;parch&#34;&#39;,
 &#39;&#34;survived&#34;&#39;,
 &#39;&#34;boat&#34;&#39;,
 &#39;&#34;ticket&#34;&#39;,
 &#39;&#34;embarked&#34;&#39;,
 &#39;&#34;home.dest&#34;&#39;,
 &#39;&#34;sibsp&#34;&#39;]</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[84]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">titanic</span><span class="o">.</span><span class="n">get_columns</span><span class="p">(</span><span class="n">exclude_columns</span> <span class="o">=</span> <span class="p">[</span><span class="s2">&quot;boat&quot;</span><span class="p">,</span> <span class="s2">&quot;embarked&quot;</span><span class="p">])</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt output_prompt">Out[84]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>[&#39;&#34;fare&#34;&#39;,
 &#39;&#34;sex&#34;&#39;,
 &#39;&#34;body&#34;&#39;,
 &#39;&#34;pclass&#34;&#39;,
 &#39;&#34;age&#34;&#39;,
 &#39;&#34;name&#34;&#39;,
 &#39;&#34;cabin&#34;&#39;,
 &#39;&#34;parch&#34;&#39;,
 &#39;&#34;survived&#34;&#39;,
 &#39;&#34;ticket&#34;&#39;,
 &#39;&#34;home.dest&#34;&#39;,
 &#39;&#34;sibsp&#34;&#39;]</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>To get only numerical columns you can use the 'numcol' which is working the same way as 'get_columns'.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[5]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span><span class="o">.</span><span class="n">numcol</span><span class="p">()</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt output_prompt">Out[5]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>[&#39;&#34;fare&#34;&#39;, &#39;&#34;body&#34;&#39;, &#39;&#34;pclass&#34;&#39;, &#39;&#34;age&#34;&#39;, &#39;&#34;parch&#34;&#39;, &#39;&#34;survived&#34;&#39;, &#39;&#34;sibsp&#34;&#39;]</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[6]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span><span class="o">.</span><span class="n">numcol</span><span class="p">(</span><span class="n">exclude_columns</span> <span class="o">=</span> <span class="p">[</span><span class="s2">&quot;body&quot;</span><span class="p">,</span> <span class="s2">&quot;sibsp&quot;</span><span class="p">])</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt output_prompt">Out[6]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>[&#39;&#34;fare&#34;&#39;, &#39;&#34;pclass&#34;&#39;, &#39;&#34;age&#34;&#39;, &#39;&#34;parch&#34;&#39;, &#39;&#34;survived&#34;&#39;]</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>For example, if you need to compute the correlation matrix of all the numerical columns except some of them. You can write the following code.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[4]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span><span class="o">.</span><span class="n">corr</span><span class="p">(</span><span class="n">columns</span> <span class="o">=</span> <span class="n">vdf</span><span class="o">.</span><span class="n">numcol</span><span class="p">(</span><span class="n">exclude_columns</span> <span class="o">=</span> <span class="p">[</span><span class="s2">&quot;parch&quot;</span><span class="p">,</span> <span class="s2">&quot;sibsp&quot;</span><span class="p">]))</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>




<div class="output_png output_subarea ">
<img src="data:image/png;base64,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
"
>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<table style="border-collapse: collapse; border: 2px solid white"><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b></b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>"fare"</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>"body"</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>"pclass"</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>"age"</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>"survived"</b></td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"fare"</b></td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">-0.0372842548942878</td><td style="border: 1px solid white;">-0.561687581153705</td><td style="border: 1px solid white;">0.178575164117464</td><td style="border: 1px solid white;">0.264150360783869</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"body"</b></td><td style="border: 1px solid white;">-0.0372842548942878</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">-0.0472355333131433</td><td style="border: 1px solid white;">0.0581765649177871</td><td style="border: 1px solid white;">nan</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"pclass"</b></td><td style="border: 1px solid white;">-0.561687581153705</td><td style="border: 1px solid white;">-0.0472355333131433</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">-0.400828642351015</td><td style="border: 1px solid white;">-0.335856950271864</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"age"</b></td><td style="border: 1px solid white;">0.178575164117464</td><td style="border: 1px solid white;">0.0581765649177871</td><td style="border: 1px solid white;">-0.400828642351015</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">-0.0422446185581737</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"survived"</b></td><td style="border: 1px solid white;">0.264150360783869</td><td style="border: 1px solid white;">nan</td><td style="border: 1px solid white;">-0.335856950271864</td><td style="border: 1px solid white;">-0.0422446185581737</td><td style="border: 1px solid white;">1</td></tr></table>
</div>

</div>

<div class="output_area">

<div class="prompt output_prompt">Out[4]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>&lt;object&gt;</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="4.-Use-the-help-function">4. Use the help function<a class="anchor-link" href="#4.-Use-the-help-function">&#182;</a></h1><p>The 'help' function is very useful when you want to know all the possible parameters.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[65]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">help</span><span class="p">(</span><span class="n">vdf</span><span class="o">.</span><span class="n">agg</span><span class="p">)</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>Help on method agg in module vertica_ml_python.vdataframe:

agg(func:list, columns:list=[]) method of vertica_ml_python.vdataframe.vDataFrame instance
    ---------------------------------------------------------------------------
    Aggregates the vDataFrame using the input functions.
    
    Parameters
    ----------
    func: list
            List of the different aggregation.
                    approx_unique  : approximative cardinality
                    count          : number of non-missing elements
                    cvar           : conditional value at risk
                    dtype          : virtual column type
                    iqr            : interquartile range
                    kurtosis       : kurtosis
                    jb             : Jarque Bera index 
                    mad            : median absolute deviation
                    mae            : mean absolute error (deviation)
                    max            : maximum
                    mean           : average
                    median         : median
                    min            : minimum
                    mode           : most occurent element
                    percent        : percent of non-missing elements
                    q%             : q quantile (ex: 50% for the median)
                    prod           : product
                    range          : difference between the max and the min
                    sem            : standard error of the mean
                    skewness       : skewness
                    sum            : sum
                    std            : standard deviation
                    topk           : kth most occurent element (ex: top1 for the mode)
                    topk_percent   : kth most occurent element density
                    unique         : cardinality (count distinct)
                    var            : variance
                            Other aggregations could work if it is part of 
                            the DB version you are using.
    columns: list, optional
            List of the vcolumns names. If empty, all the vcolumns 
            or only numerical vcolumns will be used depending on the
            aggregations.
    
    Returns
    -------
    tablesample
            An object containing the result. For more information, check out
            utilities.tablesample.
    
    See Also
    --------
    vDataFrame.analytic : Adds a new vcolumn to the vDataFrame by using an advanced 
            analytical function on a specific vcolumn.

</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="5.-Becareful-when-using-DataBase-cursors">5. Becareful when using DataBase cursors<a class="anchor-link" href="#5.-Becareful-when-using-DataBase-cursors">&#182;</a></h1><p>The increase of DB connections will increase the concurrency on the system. So be sure to not let them open and to create them by yourself. Vertica ML Python simplifies the connection process by allowing the user to create an auto-connection. This option is not the best one and it is preferable to create your own cursor when you can. Let's create a DB connection.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[67]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">import</span> <span class="nn">vertica_python</span>

<span class="n">conn_info</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;host&#39;</span><span class="p">:</span> <span class="s2">&quot;10.211.55.14&quot;</span><span class="p">,</span> 
             <span class="s1">&#39;port&#39;</span><span class="p">:</span> <span class="mi">5433</span><span class="p">,</span> 
             <span class="s1">&#39;user&#39;</span><span class="p">:</span> <span class="s2">&quot;dbadmin&quot;</span><span class="p">,</span> 
             <span class="s1">&#39;password&#39;</span><span class="p">:</span> <span class="s2">&quot;XxX&quot;</span><span class="p">,</span> 
             <span class="s1">&#39;database&#39;</span><span class="p">:</span> <span class="s2">&quot;testdb&quot;</span><span class="p">}</span>
<span class="n">conn</span> <span class="o">=</span> <span class="n">vertica_python</span><span class="o">.</span><span class="n">connect</span><span class="p">(</span><span class="o">**</span> <span class="n">conn_info</span><span class="p">)</span>
<span class="n">cur</span> <span class="o">=</span> <span class="n">conn</span><span class="o">.</span><span class="n">cursor</span><span class="p">()</span>
</pre></div>

</div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>We can use it to create a vDataFrame and do some operations.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[68]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span> <span class="o">=</span> <span class="n">vDataFrame</span><span class="p">(</span><span class="s2">&quot;public.titanic&quot;</span><span class="p">,</span> <span class="n">cur</span><span class="p">)</span>
<span class="n">vdf</span><span class="p">[</span><span class="s2">&quot;sex&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">label_encode</span><span class="p">()[</span><span class="s2">&quot;boat&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">fillna</span><span class="p">(</span><span class="n">method</span> <span class="o">=</span> <span class="s2">&quot;0ifnull&quot;</span><span class="p">)[</span><span class="s2">&quot;name&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">str_extract</span><span class="p">(</span>
    <span class="s1">&#39; ([A-Za-z]+)\.&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">eval</span><span class="p">(</span><span class="s2">&quot;family_size&quot;</span><span class="p">,</span> <span class="n">expr</span> <span class="o">=</span> <span class="s2">&quot;parch + sibsp + 1&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span>
    <span class="n">columns</span> <span class="o">=</span> <span class="p">[</span><span class="s2">&quot;cabin&quot;</span><span class="p">,</span> <span class="s2">&quot;body&quot;</span><span class="p">,</span> <span class="s2">&quot;ticket&quot;</span><span class="p">,</span> <span class="s2">&quot;home.dest&quot;</span><span class="p">])[</span><span class="s2">&quot;fare&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">fill_outliers</span><span class="p">()</span><span class="o">.</span><span class="n">fillna</span><span class="p">()</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>795 element(s) was/were filled
</pre>
</div>
</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<table style="border-collapse: collapse; border: 2px solid white"><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b></b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>survived</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>boat</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>embarked</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>sibsp</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>fare</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>sex</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>pclass</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>age</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>name</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>parch</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>family_size</b></td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>0</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">151.5500000000000</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">2.0000000000000</td><td style="border: 1px solid white;"> Miss.</td><td style="border: 1px solid white;">2</td><td style="border: 1px solid white;">4</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>1</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">151.5500000000000</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">30.0000000000000</td><td style="border: 1px solid white;"> Mr.</td><td style="border: 1px solid white;">2</td><td style="border: 1px solid white;">4</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>2</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">151.5500000000000</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">25.0000000000000</td><td style="border: 1px solid white;"> Mrs.</td><td style="border: 1px solid white;">2</td><td style="border: 1px solid white;">4</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>3</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0E-13</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">39.0000000000000</td><td style="border: 1px solid white;"> Mr.</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">1</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>4</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">C</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">49.5042000000000</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">71.0000000000000</td><td style="border: 1px solid white;"> Mr.</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">1</td></tr><tr><td style="border-top: 1px solid white;background-color:#263133;color:white"></td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td></tr></table>
</div>

</div>

<div class="output_area">

<div class="prompt output_prompt">Out[68]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>&lt;object&gt;  Name: titanic, Number of rows: 1234, Number of columns: 11</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>We can close the connection when we are done.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[69]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">cur</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>
<span class="n">conn</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>
</pre></div>

</div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>It is very important to follow the previous process when you are working in an environment with multiple users.</p>
<h1 id="6.-Understand-the-methods-complexity">6. Understand the methods complexity<a class="anchor-link" href="#6.-Understand-the-methods-complexity">&#182;</a></h1><p>Some techniques are expensive in terms of computations. Using for example 'kendall' correlation is very expensive compared to 'pearson'. Due to the fact that 'kendall' correlation is using a cross join, its complexity is O(n*n) (n corresponding to the number of rows). Let's see it in a well known dataset.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[73]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span><span class="o">.</span><span class="n">time_on_off</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Pearson&quot;</span><span class="p">)</span>
<span class="n">vdf</span><span class="o">.</span><span class="n">corr</span><span class="p">(</span><span class="n">method</span> <span class="o">=</span> <span class="s2">&quot;pearson&quot;</span><span class="p">,</span> <span class="n">show</span> <span class="o">=</span> <span class="kc">False</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Kendall&quot;</span><span class="p">)</span>
<span class="n">vdf</span><span class="o">.</span><span class="n">corr</span><span class="p">(</span><span class="n">method</span> <span class="o">=</span> <span class="s2">&quot;kendall&quot;</span><span class="p">,</span> <span class="n">show</span> <span class="o">=</span> <span class="kc">False</span><span class="p">)</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>Pearson
</pre>
</div>
</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<div><b>Elapsed Time : </b> 0.024621963500976562</div>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<div style = 'border : 1px dashed black; width : 100%'></div>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>Kendall
</pre>
</div>
</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<div><b>Elapsed Time : </b> 2.0850696563720703</div>
</div>

</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<div style = 'border : 1px dashed black; width : 100%'></div>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>Kendall Correlation Matrix is much more time (around 100 times more than Pearson) to be computed because of its complexity.</p>
<h1 id="7.-Limit-the-number-of-elements-to-plot">7. Limit the number of elements to plot<a class="anchor-link" href="#7.-Limit-the-number-of-elements-to-plot">&#182;</a></h1><p>Graphics are a powerful way to understand the data but they are used to summarize the information. Their purpose is not to draw millions of elements from which we could not extract information. Human mind likes when it is easy. Let's draw a multi-histogram where one of the column is categorical with thousand of categories.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[76]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">titanic</span><span class="o">.</span><span class="n">hist</span><span class="p">([</span><span class="s2">&quot;name&quot;</span><span class="p">,</span> <span class="s2">&quot;survived&quot;</span><span class="p">])</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>




<div class="output_png output_subarea ">
"
>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>Vertica ML Python will try to draw it but it could take time if the dataset is huge and it could be totally useless whereas drawing graphics with few categories can give us much more information.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[77]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">titanic</span><span class="o">.</span><span class="n">hist</span><span class="p">([</span><span class="s2">&quot;pclass&quot;</span><span class="p">,</span> <span class="s2">&quot;survived&quot;</span><span class="p">])</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>




<div class="output_png output_subarea ">
<img src="data:image/png;base64,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eMUrvveKV7xi+YoVK2rVqlW56aabpu+WGNxzzz116aWXfjVJvvKVrzzooosuevCRRx75owsuuGCnpz3tabfPnTv3Z/M+nve8593xute9bq877rjjATvuuOPq8847b+ff/M3fXP7d7353m7e//e0P/+d//uev77jjjqtPO+20h73tbW9b8MY3vvG7r33ta/f+xCc+cc3+++9/17HHHvuzcPLSl770tvt73jPtwXhXkhcm+UZVva2qJjqODAAAtjRPecpTfvK3f/u3Dz/ttNMe9s1vfnPu9ttvv85J4ccdd9zyNY//63/9r7edd955OyfJRz7ykfnHHXfcvULAtttum6c//el3nH/++Tvdc889ufjii3d6wQte8MPPfvaz21977bXznvnMZ+53yCGHHHD++efvcsMNN8z98pe/PG+33Xa768ADD7zrAQ94QI4//vhbe5znjAJGa+3TrbXfSbIwyXVJPl1V/1FVL62q+0xdAABA8vKXv3z5eeedt2zevHmrjz322H3/6Z/+6cHbbrtta+3nOWPFihX3uj7fYYcdfjZ66LjjjvvhZz/72Z2+//3vz7nqqqsedOSRR94x9RgveMELll944YXzlyxZsuOBBx7404c85CGrW2t56lOfesfll19+9eWXX371lVdeedU555xz/aTOc8ZzMKpqlyQvSfLyJJcn+duMAsenJlIZAABsQb72ta/NfexjH3vXKaec8v3DDjvsh1/60pceuNtuu61cvnz5Nt/73vfm3HnnnfXpT396p7Vtv9NOO60+6KCDfvIHf/AHez772c++fZttfnG2w+GHH/6jr371qw/6h3/4h12PPfbY5Uny9Kc//Sdf/OIXd7j66qu3S0bzN6688srtHv/4x6/4zne+M/erX/3qdkly3nnnze9xnjOdg3FhkscmeX+S32it3Tws+lBVXdqjEAAA2JJ98IMfnH/BBRfssu2227Zdd931nlNPPfXmuXPntte85jU3P/3pT9//l37pl+551KMeteK+9vGbv/mbt73qVa965AUXXHDNdMu32WabPPvZz779wgsv3OWcc865Lkke/vCHr3znO9953QknnPDIu+++u5Lk9a9//U0HHXTQXX/zN39z/bHHHvvoefPmrX7yk5/84x//+MdzNvQ8a7xLZq0rVR3ZWlsypW271tpdG1pALwsXLmyf+9znZrsMAGAT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
"
>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>Try to always check your variables cardinality before drawing expensive graphics.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[78]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">titanic</span><span class="o">.</span><span class="n">nunique</span><span class="p">()</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<table style="border-collapse: collapse; border: 2px solid white"><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b></b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>unique</b></td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"fare"</b></td><td style="border: 1px solid white;">277.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"sex"</b></td><td style="border: 1px solid white;">2.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"body"</b></td><td style="border: 1px solid white;">118.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"pclass"</b></td><td style="border: 1px solid white;">3.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"age"</b></td><td style="border: 1px solid white;">96.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"name"</b></td><td style="border: 1px solid white;">1232.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"cabin"</b></td><td style="border: 1px solid white;">182.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"parch"</b></td><td style="border: 1px solid white;">8.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"survived"</b></td><td style="border: 1px solid white;">2.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"boat"</b></td><td style="border: 1px solid white;">26.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"ticket"</b></td><td style="border: 1px solid white;">887.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"embarked"</b></td><td style="border: 1px solid white;">3.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"home.dest"</b></td><td style="border: 1px solid white;">359.0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>"sibsp"</b></td><td style="border: 1px solid white;">7.0</td></tr></table>
</div>

</div>

<div class="output_area">

<div class="prompt output_prompt">Out[78]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>&lt;object&gt;</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="8.-Filter-the-data-you-don't-need">8. Filter the data you don't need<a class="anchor-link" href="#8.-Filter-the-data-you-don't-need">&#182;</a></h1>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>Filtering should be the first action you do when preparing your data. It will drastically improve the performance of the process as you will avoid useless computation on elements you do not use later. In the following example, we decided to do a study on Titanic passengers who do not have access to a lifeboat.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[79]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="s2">&quot;boat IS NOT NULL&quot;</span><span class="p">)</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>795 element(s) was/were filtered
</pre>
</div>
</div>

<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<table style="border-collapse: collapse; border: 2px solid white"><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b></b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>fare</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>sex</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>body</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>pclass</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>age</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>name</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>cabin</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>parch</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>survived</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>boat</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>ticket</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>embarked</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>home.dest</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>sibsp</b></td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>0</b></td><td style="border: 1px solid white;">75.2417</td><td style="border: 1px solid white;">male</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">36.0</td><td style="border: 1px solid white;">Beattie, Mr. Thomson</td><td style="border: 1px solid white;">C6</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">A</td><td style="border: 1px solid white;">13050</td><td style="border: 1px solid white;">C</td><td style="border: 1px solid white;">Winnipeg, MN</td><td style="border: 1px solid white;">0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>1</b></td><td style="border: 1px solid white;">30.6958</td><td style="border: 1px solid white;">male</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">Hoyt, Mr. William Fisher</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">14</td><td style="border: 1px solid white;">PC 17600</td><td style="border: 1px solid white;">C</td><td style="border: 1px solid white;">New York, NY</td><td style="border: 1px solid white;">0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>2</b></td><td style="border: 1px solid white;">211.3375</td><td style="border: 1px solid white;">female</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">29.0</td><td style="border: 1px solid white;">Allen, Miss. Elisabeth Walton</td><td style="border: 1px solid white;">B5</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">2</td><td style="border: 1px solid white;">24160</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">St Louis, MO</td><td style="border: 1px solid white;">0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>3</b></td><td style="border: 1px solid white;">151.55</td><td style="border: 1px solid white;">male</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">0.92</td><td style="border: 1px solid white;">Allison, Master. Hudson Trevor</td><td style="border: 1px solid white;">C22 C26</td><td style="border: 1px solid white;">2</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">11</td><td style="border: 1px solid white;">113781</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">Montreal, PQ / Chesterville, ON</td><td style="border: 1px solid white;">1</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>4</b></td><td style="border: 1px solid white;">26.55</td><td style="border: 1px solid white;">male</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">48.0</td><td style="border: 1px solid white;">Anderson, Mr. Harry</td><td style="border: 1px solid white;">E12</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">3</td><td style="border: 1px solid white;">19952</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">New York, NY</td><td style="border: 1px solid white;">0</td></tr><tr><td style="border-top: 1px solid white;background-color:#263133;color:white"></td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td></tr></table>
</div>

</div>

<div class="output_area">

<div class="prompt output_prompt">Out[79]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>&lt;object&gt;  Name: titanic, Number of rows: 439, Number of columns: 14</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>It is not needed to think this way when we are dealing with small volumes of data but it is really important to think about filtering useless information first when dealing with huge volumes of data.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="9.-Filter-the-columns-you-don't-need">9. Filter the columns you don't need<a class="anchor-link" href="#9.-Filter-the-columns-you-don't-need">&#182;</a></h1>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>As explained before, using only the needed columns in the different methods is one the keys to increase performance. To avoid, writing more codes to exclude useless column it is possible to filter them using the 'drop' method.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[7]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">vdf</span><span class="o">.</span><span class="n">drop</span><span class="p">([</span><span class="s2">&quot;name&quot;</span><span class="p">,</span> <span class="s2">&quot;boat&quot;</span><span class="p">])</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>



<div class="output_html rendered_html output_subarea ">
<table style="border-collapse: collapse; border: 2px solid white"><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b></b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>survived</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>ticket</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>embarked</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>home.dest</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>sibsp</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>fare</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>sex</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>body</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>pclass</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>age</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>cabin</b></td><td style="font-size:1.02em;background-color:#263133;color:white"><b>parch</b></td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>0</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">113781</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">Montreal, PQ / Chesterville, ON</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">151.55</td><td style="border: 1px solid white;">female</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">2.0</td><td style="border: 1px solid white;">C22 C26</td><td style="border: 1px solid white;">2</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>1</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">113781</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">Montreal, PQ / Chesterville, ON</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">151.55</td><td style="border: 1px solid white;">male</td><td style="border: 1px solid white;">135</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">30.0</td><td style="border: 1px solid white;">C22 C26</td><td style="border: 1px solid white;">2</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>2</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">113781</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">Montreal, PQ / Chesterville, ON</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">151.55</td><td style="border: 1px solid white;">female</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">25.0</td><td style="border: 1px solid white;">C22 C26</td><td style="border: 1px solid white;">2</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>3</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">112050</td><td style="border: 1px solid white;">S</td><td style="border: 1px solid white;">Belfast, NI</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">0.0</td><td style="border: 1px solid white;">male</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">39.0</td><td style="border: 1px solid white;">A36</td><td style="border: 1px solid white;">0</td></tr><tr ><td style="font-size:1.02em;background-color:#263133;color:white"><b>4</b></td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">PC 17609</td><td style="border: 1px solid white;">C</td><td style="border: 1px solid white;">Montevideo, Uruguay</td><td style="border: 1px solid white;">0</td><td style="border: 1px solid white;">49.5042</td><td style="border: 1px solid white;">male</td><td style="border: 1px solid white;">22</td><td style="border: 1px solid white;">1</td><td style="border: 1px solid white;">71.0</td><td style="border: 1px solid white;">None</td><td style="border: 1px solid white;">0</td></tr><tr><td style="border-top: 1px solid white;background-color:#263133;color:white"></td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td><td style="border: 1px solid white;">...</td></tr></table>
</div>

</div>

<div class="output_area">

<div class="prompt output_prompt">Out[7]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>&lt;object&gt;  Name: titanic, Number of rows: 1234, Number of columns: 12</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>By using the 'drop' method, Vertica ML Python will simply not use the input columns in the next SQL code generation.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[8]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="nb">print</span><span class="p">(</span><span class="n">vdf</span><span class="o">.</span><span class="n">current_relation</span><span class="p">())</span>
</pre></div>

</div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

<div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>(
   SELECT
     &#34;survived&#34;,
     &#34;ticket&#34;,
     &#34;embarked&#34;,
     &#34;home.dest&#34;,
     &#34;sibsp&#34;,
     &#34;fare&#34;,
     &#34;sex&#34;,
     &#34;body&#34;,
     &#34;pclass&#34;,
     &#34;age&#34;,
     &#34;cabin&#34;,
     &#34;parch&#34; 
   FROM
 &#34;public&#34;.&#34;titanic&#34;) 
VERTICA_ML_PYTHON_SUBTABLE
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="10.-Enjoy-:p">10. Enjoy :p<a class="anchor-link" href="#10.-Enjoy-:p">&#182;</a></h1>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<p>Even in your own personal machine you can now deal with volume of data you could not in the past. Learn how to optimize your Vertica DB and start playing with Vertica ML Python. The next lesson will teach you how to ingest your first datasets.</p>

</div>
</div>
</div>