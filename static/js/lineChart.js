//namespace

d3.custom = {};


//linechart under the module namespace
d3.custom.lineChart = function module() {
    //define some private vars
    var mobileThreshold = 350,
        tickSize = 13,
        yAxisLabel = "This is the Y Axis",
        strokeWidth = 5,
        strokeColor = "#28556F", //dark blue
        xAccess = function(d) { return d.year; },
        yAccess = function(d) { return d.value; },
        hover = "true";

    //aspect ratio
    var aspect = {
        width: 16,
        height: 9
    };

    var margin = {
        top: 10,
        right: 10,
        bottom: 30,
        left: 50
    };

    var tooltip = {
        value: "", //unused for now.  Only useful if more than two columns of data are present
        string: "",
        format: d3.format("f") //fixed to two decimal places
    };
    //formats
    var xFormat = d3.format("f") //fixed
    yAxisFormat = d3.format("s"); //scientific

    var _data = [];
    //scales
    var xScale = d3.scale.linear(),
        yScale = d3.scale.linear(),
        yMax = null;


    //everything below this is private
    function exports(_selection) {
        _selection.each(function(_data) {

            var selection = "#" + [_selection[0][0].id];

            console.log(_selection);
            console.log(_data);

            // Convert data to standard representation greedily;
            // this is needed for nondeterministic accessors.
            _data = _data.map(function(d, i) {
                return [xAccess.call(_data, d, i), yAccess.call(_data, d, i)];
            });

            //find width of container
            var width = $(this).width() - margin.left - margin.right;

            //set height
            var height = Math.ceil((width * aspect.height) / aspect.width) - margin.top - margin.bottom;
            //mobile checks

            function ifMobile(w) {
                if (w < mobileThreshold) {
                    tickSize = Math.ceil(tickSize / 2);
                    strokeWidth = Math.ceil(strokeWidth / 2);
                    console.log("Mobile Threshold Reached");
                    fontSize = "10px sans-serif";
                } else {
                    tickSize = tickSize;
                    strokeWidth = strokeWidth;
                    fontSize = "12px sans-serif";
                }
            }

            //set mobile variables
            ifMobile(width);

            //scales
            var x = xScale.range([0, width])
                .domain(d3.extent(_data, function(d) { return d[0]; }));

            var y = yScale.range([height, 0]).domain([0, d3.max(_data, function(d) { return d[1]; })]); //ymax is a function or a number	

            //check to see if user has set an arbitrary max value
            yMax ? y.domain([0, yMax]) : null;

            //define axes
            var xAxis = d3.svg.axis()
                .ticks(tickSize)
                .tickFormat(xFormat)
                .tickSize(8, 8, 0)
                .orient("bottom")
                .scale(x);

            var yAxis = d3.svg.axis()
                .orient("left")
                .tickFormat(yAxisFormat)
                .ticks(tickSize)
                .tickSize(5, 5, 0)
                .scale(y);

            //define line
            var line = d3.svg.line()
                .x(function(d) { return x(d[0]); })
                .y(function(d) { return y(d[1]); });

            //look for svg and select
            var svg = d3.select(this).selectAll("svg").data([_data]);
            //skeleton chart
            var gEnter = svg.enter().append("svg").append("g");
            gEnter.append("g").attr("class", "x grid");
            gEnter.append("g").attr("class", "y grid");
            gEnter.append("path").attr("class", "line");
            gEnter.append("g").attr("class", "x axis");
            gEnter.append("g").attr("class", "y axis");
            gEnter.append("g").attr("class", "focus");
            gEnter.append("g").attr("class", "overlay");


            //update outer skeleton
            svg.attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom);

            //update inner skeleton (everything is appended to this)
            var g = svg.select("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            //grid
            var x_axis_grid = function() { return xAxis; };

            var y_axis_grid = function() { return yAxis; };

            g.select(".line").attr("d", line)
                .style("stroke-width", strokeWidth)
                .style("stroke", strokeColor);

            g.select(".x.axis")
                .attr("transform", "translate(0," + height + ")")
                .style("font", fontSize)
                .call(xAxis);

            g.select(".y.axis")
                .call(yAxis)
                .style("font", fontSize)
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", -margin.left + 10)
                .attr("x", -10)
                .attr("dy", "0.71em")
                .style("text-anchor", "end")
                .style("font", fontSize)
                .text(yAxisLabel);

            //grid

            g.select(".y.grid")
                .call(y_axis_grid()
                    .tickSize(-width, 0, 0)
                    .tickFormat(" "));

            g.select(".x.grid")
                .call(x_axis_grid()
                    .tickSize(height, 0, 0)
                    .tickFormat(" "));
            //end grid

            //mouseover effects
            var focus = g.select(".focus")
                .style("display", "none");

            focus.append("circle")
                .attr("r", 6)
                .style("stroke", strokeColor);

            focus.append("text")
                .attr("x", 9)
                .attr("dy", ".35em");

            var div = d3.select(this).append("div")
                .attr("class", "tooltip")
                .style("opacity", 0)
                .style("font", fontSize);

            //mouseover overlay
            g.select(".overlay").append("rect")
                .attr("width", width)
                .attr("height", height)
                .on("mouseover", function() {
                    if (hover == "false") {
                        return;
                    }
                    focus.style("display", null);
                })
                .on("mouseout",
                    function(d) {
                        focus.style("display", "none");
                        div.transition()
                            .duration(500)
                            .style("opacity", 0);
                    })
                .on("mousemove", mousemove);

            var bisectDate = d3.bisector(function(d) { return d[0]; }).left;

            function mousemove(d) {
                if (hover == "false") {
                    return;
                }

                var x0 = x.invert(d3.mouse(this)[0]),
                    i = bisectDate(_data, x0, 1),
                    d0 = _data[i - 1],
                    d1 = _data[i],
                    d = x0 - d0[d[0]] > d1[d[0]] - x0 ? d1 : d0;

                focus.attr("transform", "translate(" + x(d[0]) + "," + y(d[1]) + ")");
                //show div
                d3.select(selection).selectAll(".tooltip").transition()
                    .duration(200)
                    .style("opacity", 0.9);

                d3.select(selection).selectAll(".tooltip")
                    .html(tooltip.format(d[1]) + " strikes")
                    .style("left", x(d[0]) + margin.left + $(selection).position().left + "px")
                    .style("top", y(d[1]) + $(selection).position().top + -20 + "px");

                d3.select(selection).selectAll(".tooltip")
                    .html(tooltip.format(d[1]) + " " + tooltip.string);

            } //end mouseover effects
        });

    } //end of exports

    exports.xAccess = function(_x) {
        //takes a function in the form of function(d {return d.value; }
        if (!arguments.length) return xAccess;
        xAccess = _x;
        return this;
    };

    exports.yAccess = function(_x) {
        //takes a function in the form of function(d {return d.value; }
        if (!arguments.length) return yAccess;
        yAccess = _x;
        return this;
    };

    exports.tooltipValue = function(_x) {
        //not used right now
        if (!arguments.length) return tooltip.value;
        tooltip.value = _x;
        return this;
    };

    exports.tooltipString = function(_x) {
        //takes a string in the form "unit"
        if (!arguments.length) return tooltip.string;
        tooltip.string = _x;
        return this;
    };

    exports.strokeWidth = function(_x) {
        //takes a number
        if (!arguments.length) return strokeWidth;
        strokeWidth = _x;
        return this;
    };

    exports.strokeColor = function(_x) {
        //takes a css color or hex
        if (!arguments.length) return strokeColor;
        strokeColor = _x;
        return this;
    };

    exports.tooltipFormat = function(_x) {
        //takes a d3.format method in the form of d3.format("0.2f")
        if (!arguments.length) return tooltip.format;
        tooltip.format = _x;
        return this;
    };

    exports.xFormat = function(_x) {
        //takes a format method in the form of d3.format("0.2f")
        if (!arguments.length) return xFormat;
        xFormat = _x;
        return this;
    };

    exports.yAxisLabel = function(_x) {
        //takes a string
        if (!arguments.length) return yAxisLabel;
        yAxisLabel = _x;
        return this;
    };

    exports.tickSize = function(_x) {
        //takes a number
        if (!arguments.length) return tickSize;
        tickSize = _x;
        return this;
    };

    exports.margin = function(_x) {
        //takes a margin object in the form of {top: 10,right: 10, bottom: 30, left: 50}; 
        if (!arguments.length) return margin;
        margin = _x;
        return this;
    };

    exports.marginLeft = function(_x) {
        //takes a number
        if (!arguments.length) return margin.left;
        margin.left = _x;
        return this;
    };

    exports.xScale = function(_x) {
        //takes a d3 scale in the form of d3.scale.linear()
        if (!arguments.length) return xScale;
        xScale = _x;
        return this;
    };

    exports.yAxisFormat = function(_x) {
        //a format in the form of d3.format("string");
        if (!arguments.length) return yAxisFormat;
        yAxisFormat = _x;
        return this;
    };

    exports.yMax = function(_x) {
        //takes a number; 
        if (!arguments.length) return yMax;
        yMax = _x;
        return this;
    };

    exports.yScale = function(_x) {
        //takes a scale in the format of d3.scale.linear();
        if (!arguments.length) return yScale;
        yScale = _x;
        return this;
    };

    exports.hover = function(_x) {
        //takes bool
        if (!arguments.length) return hover;
        hover = _x;
        return this;
    };

    exports.aspect = function(_x, _y) {
        //takes two numbers to represent an aspect ratio. Looks best with 16,9 or 4,3
        if (!arguments.length) return aspec;
        aspect.width = _x;
        aspect.height = _y;
        return this;
    }

    return exports;

}; //end

/////////////// add line module ///////////
d3.custom.addLine = function module() {
    //private vars
    var mobileThreshold = 350,
        tickSize = 13,
        yAxisLabel = "This is the Y Axis",
        strokeWidth = 5,
        strokeColor = "#28556F", //dark blue
        xAccess = function(d) { return d.year; },
        yAccess = function(d) { return d.value; };

    //aspect ratio
    var aspect = {
        width: 16,
        height: 9
    }

    var margin = {
        top: 10,
        right: 10,
        bottom: 30,
        left: 50
    };

    //formats
    var xFormat = d3.format("f"),
        yAxisFormat = d3.format("s");

    var _data = [];
    //scales
    var xScale = d3.scale.linear(),
        yScale = d3.scale.linear(),
        yMax = d3.max(_data, function(d) { return d[1]; });

    function exports(_selection) {
        _selection.each(function(_data) {

            _data = _data.map(function(d, i) {
                return [xAccess.call(_data, d, i), yAccess.call(_data, d, i)];
            });

            //find width of container
            var width = $(this).width() - margin.left - margin.right;

            //set height
            var height = Math.ceil((width * aspect.height) / aspect.width) - margin.top - margin.bottom;

            //change on mobile
            function ifMobile(w) {
                if (w < mobileThreshold) {
                    strokeWidth = Math.ceil(strokeWidth / 2);
                    console.log("Mobile Threshold Reached");
                } else {
                    strokeWidth = strokeWidth;
                }
            }

            //set mobile variables
            ifMobile(width);

            //scales
            var x = xScale.range([0, width])
                .domain(d3.extent(_data, function(d) { return d[0]; }));

            var y = yScale.range([height, 0]).domain([0, yMax]);

            //define line
            var line = d3.svg.line()
                .x(function(d) { return x(d[0]); })
                .y(function(d) { return y(d[1]); });
            //look for svg and select
            var svg = d3.select(this).selectAll("svg");

            var g = svg.select("g");

            g.append("path")
                .datum(_data)
                .attr("class", "line")
                .attr("d", line)
                .style("stroke-width", strokeWidth)
                .style("stroke", strokeColor);
        }); //end selection.each
    } //end exports

    exports.xAccess = function(_x) {
        //takes a function in the form of function(d {return d.value; }
        if (!arguments.length) return xAccess;
        xAccess = _x;
        return this;
    };

    exports.yAccess = function(_x) {
        //takes a function in the form of function(d {return d.value; }
        if (!arguments.length) return yAccess;
        yAccess = _x;
        return this;
    };

    exports.tooltipValue = function(_x) {
        //not used right now
        if (!arguments.length) return tooltip.value;
        tooltip.value = _x;
        return this;
    };

    exports.tooltipString = function(_x) {
        //takes a string in the form "unit"
        if (!arguments.length) return tooltip.string;
        tooltip.string = _x;
        return this;
    };

    exports.strokeWidth = function(_x) {
        //takes a number
        if (!arguments.length) return strokeWidth;
        strokeWidth = _x;
        return this;
    };

    exports.strokeColor = function(_x) {
        //takes a css color or hex
        if (!arguments.length) return strokeColor;
        strokeColor = _x;
        return this;
    };


    exports.yMax = function(_x) {
        //takes a number; 
        if (!arguments.length) return yMax;
        yMax = _x;
        return this;
    };
    return exports;
}; //end module