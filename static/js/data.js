var wordData = ''
var sentiments = ''
var pweight = 0
var nweight = 0

function checkData() {
var keyword = document.getElementById("Keyword").value;
var count = document.getElementById("Count").value;
var city = document.getElementById("City").value;


if (keyword == "" || count == "" || city == "") {
    window.alert("Please enter all details");
} else {
    $.ajax({
         url: '/getDetails',
         data : {'keyword' : keyword , 'count' : count , 'city' : city },
         type: 'POST',
         success: function(response){
             wordData = JSON.parse(response)
             wordCloud();
             pieChart();
             alert("Success!!!")
         },
         error: function(error){
            console.log(error);
            alert("Error!!!")
         }
   });
}

//Word Cloud
function wordCloud() {
sentiments = getWordCloud()
$(document).ready(function() {
         $("#wordCloud").jQCloud(sentiments);
});
}

function getWordCloud() {
    sentiment = [];
    for (var i = 2; i < wordData.length; i++ ) {
        if (wordData[i].sentiment == "positive") {
            text = wordData[i].text.fontcolor('green')
            sentiment.push({text :  text , weight : (wordData[i].weight)});
        } else {
            text = wordData[i].text.fontcolor('red')
            sentiment.push({text :  text , weight : (wordData[i].weight)});
        }
    }
    return sentiment;
};

//Pie Chart

function pieChart() {
piedata = getpieChart()
$(document).ready(function(){
  var plot1 = jQuery.jqplot ('piechart', [piedata],
    {
      seriesDefaults: {
        renderer: jQuery.jqplot.PieRenderer,
        rendererOptions: {
          showDataLabels: true
        }
      },
      legend: { show:true, location: 'e' }
    }
  );
});
}

function getpieChart() {
piedata = [];
alert(wordData[0].total_polarity)
    if (wordData[0].total_polarity > 1) {
        document.getElementById("piechart").style.backgroundColor = "green";
    } else {
        document.getElementById("piechart").style.backgroundColor = "red";
    }
    for (var i = 1 ; i < wordData.length ; i++) {
        if (wordData[i].sentiment == "positive") {
            pweight = pweight + wordData[i].weight;
        } else {
            nweight = nweight + wordData[i].weight;
        }
    }
    piedata.push(['Positive' , pweight])
    piedata.push(['Negative' , nweight])
    return piedata
};
}