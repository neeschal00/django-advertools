import advertools as adv
import pandas as pd

pd.options.display.max_colwidth = 120
import plotly.express as px

# %% ../nbs/02_url_structure.ipynb 4
_texttemplate = "<b>%{label} </b><br><br>Directory: <b>%{parent}/%{label}</b><br>Count: %{value:,}<br>%{percentParent:.1%} of %{parent}<br>"

# %% ../nbs/02_url_structure.ipynb 5


def value_counts_plus(
    series,
    dropna=False,
    show_top=10,
    sort_others=False,
    style=True,
    size=10,
    thousands=",",
    decimal=".",
    name="data",
    background_gradient="cividis",
):
    """
    Provide a few ways of showing counts of values of items in ``series``.

    Parameters
    ----------
    series : pandas Series or list
        A sequence of items to count.
    dropna : bool
        Whether or not to drop missing values.
    show_top : int
        How many of the top rows to display.
    sort_others : bool
        Whether or not to place "Others" in the bottom (default) or in its
        sorted order position.
    style : bool
        Whether or not to style values for easier reading. If set to ``True``
        the result would not be a DataFrame, and cannot be further manipulated.
        Set the value to ``False`` to get aDataFrame as the return value.
    size : int
        The size in points of the font of the table. This results in the whole
        table being resized.
    thousands : str
        The character to use to separate thousands if `style=True`. Defaults to
        `,` but you can change to `.` or space, or any oher character you want.
    decimal : str
        The character to use to display decimal number if `style=True`. Defaults to
        `.` but you can change to `,`or any oher character you want.

    name : str
        The name of the column that you want displayed in the final table. It
        appears in the caption and defaults to "data".
    background_gradient: str
        The name of the color map to be used as the gradient. Many color maps
        are available: cividis, viridis, copper, cool, magma, and more. You can
        reverse the color by appending _r to the end of the colormap name
        cividis_r for example. Enter a random string to get an error message
        with all available colormaps.

    Returns
    -------
    value_counts_df : pandas.io.formats.style.Styler
        A DataFrame showing counts based on the provided arguments
    """
    final_col_names = ["count", "cum_count", "perc", "cum_perc"]
    if name in final_col_names:
        raise ValueError(
            f"Please make sure you use a name other than {final_col_names}"
        )
    val_counts = (
        pd.Series(series).rename(name).value_counts(dropna=dropna).reset_index()
    )
    val_counts.columns = [name, "count"]
    if len(val_counts) > show_top:
        others_df = pd.DataFrame(
            {name: ["Others:"], "count": val_counts[show_top:]["count"].sum()},
            index=[show_top],
        )
        val_counts = pd.concat([val_counts[:show_top], others_df])
        if sort_others:
            val_counts = val_counts.sort_values(by=["count"], ascending=False)

    count_df = val_counts.assign(
        cum_count=lambda df: df["count"].cumsum(),
        perc=lambda df: df["count"].div(df["count"].sum()),
        cum_perc=lambda df: df["perc"].cumsum(),
    )
    if not style:
        return count_df
    count_df.index = range(1, len(count_df) + 1)
    count_df.columns = [name, "count", "cum. count", "%", "cum. %"]
    return (
        count_df.style.format(
            {
                "count": "{:>,}",
                "cum. count": "{:>,}",
                "%": "{:>.1%}",
                "cum. %": "{:>.1%}",
            },
            thousands=thousands,
            decimal=decimal,
        )
        .background_gradient(background_gradient)
        .highlight_null()
        .set_caption(f"<h2>Counts of <b>{name}</b></h2>")
        .set_table_attributes(f"style=font-size:{size}pt;")
    )


def url_structure(
    df,
    items_per_level=10,
    height=600,
    width=None,
    theme="none",
    domain="",
    title="URL Structure",
):
    """
    Create a treemap for the first two URL path directories `example.com/dir_1/dir_2/`.

    Parameters
    ----------
    df : dataframe
        data frame object.
    items_per_level : int
        The number of items to display for each level of the treemap. All other
        items will be grouped under a special item called "Others".
    height : int
        The height of the chart in pixels.
    width : int
        The width of the chart in pixels.
    theme : str
        Name of theme to use for the chart. Available themes:
            ggplot2, seaborn, simple_white, plotly, plotly_white, plotly_dark,
            presentation, xgridoff, ygridoff, gridon, none.
    domain : str
        The main domain of the URL list. This will be displayed at the top
        panel in the treemap to display values like a breadcrumb.
    title: str
        The title of the figure. You can use/include the following HTML tags in
        the title: `<a>`, `<b>`, `<br>`, `<i>`, `<sub>`, `<sup>`

    Returns
    -------
    url_structure_treemap : plotly.graph_objects.Figure
    """
    urldf = df
    dir1_top_n = urldf["dir_1"].value_counts().head(items_per_level).index.tolist() + [
        "Others:"
    ]
    urldf["dir_1_clean"] = [x if x in dir1_top_n else "Others:" for x in urldf["dir_1"]]
    top_n_df = pd.DataFrame(dir1_top_n, columns=["dir_1_top_n"])

    dir2_valcounts = []

    for top_n in top_n_df["dir_1_top_n"]:
        tempdf = urldf[urldf["dir_1_clean"].eq(top_n)]
        valcountsdf = value_counts_plus(
            tempdf["dir_2"], show_top=items_per_level, style=False
        )
        valcountsdf = valcountsdf.assign(dir_1_value=top_n)
        dir2_valcounts.append(valcountsdf)
    dir2_df = pd.concat(dir2_valcounts, ignore_index=True)[
        ["data", "count", "dir_1_value"]
    ]
    treemap_df = pd.merge(
        top_n_df, dir2_df, left_on="dir_1_top_n", right_on="dir_1_value", how="left"
    )
    fig = px.treemap(
        treemap_df.dropna(),
        path=[px.Constant(domain), "dir_1_top_n", "data"],
        branchvalues="total",
        maxdepth=2,
        width=width,
        height=height,
        title=title,
        template=theme,
        values="count",
    )
    fig.data[0].marker.line.width = 0.01
    fig.data[0].marker.pad = dict.fromkeys("lrbt", 0)
    fig.data[0]["texttemplate"] = _texttemplate
    fig.data[0]["hovertemplate"] = _texttemplate
    fig.update_traces(pathbar={"edgeshape": "/"})
    return fig
