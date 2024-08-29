<template>
  <div
    class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded bg-blueGray-700"
  >
    <div class="rounded-t mb-0 px-4 py-3 bg-transparent">
      <div class="flex flex-wrap items-center">
        <div class="relative w-full max-w-full flex-grow flex-1">
          <h6 class="uppercase text-blueGray-100 mb-1 text-xs font-semibold">
            Performance
          </h6>
          <h2 class="text-white text-xl font-semibold">
            Sales vs. Month
          </h2>
        </div>
      </div>
    </div>
    <div class="p-4 flex-auto">
      <!-- Chart -->
      <div class="relative h-350-px">
        <canvas id="line-chart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js";

export default {
  data() {
    return {
      // yearData: {
      //   currYearData: Array(12).fill(0),
      //   prevYearData: Array(12).fill(0)
      // },
      years: {
        currYear: new Date().getFullYear(),
        prevYear: new Date().getFullYear()-1
      }
    };
  },
  // methods: {
  //   async loadData() {
  //     const orderData = await axios.get('https://project-3-full-stack-agile-web-902-team-3-jctc.onrender.com/order')
  //     orderData.data.forEach(({ total, timestamp, status }) => {
  //       const month = timestamp.split('-')[1];
  //       const year = timestamp.split('-')[0];
  //       if (year == this.years.currYear && status == 0) {
  //         this.yearData.currYearData[month-1] += total;
  //       }
  //       else if (year == this.years.prevYear && status == 0) {
  //         this.yearData.prevYearData[month-1] += total;
  //       }
  //     });
  //   }
  // },

  props: {
    data: Object
  },
  mounted: function () {
    //this.loadData()
    this.$nextTick(function () {
      var config = {
        type: "line",
        data: {
          labels: [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
          ],
          datasets: [
            {
              label: this.years.currYear,
              backgroundColor: "#4c51bf",
              borderColor: "#4c51bf",
              //data: [65, 78, 66, 44, 56, 67, 75],
              //data: this.yearData.currYearData,
              data: this.$props.data.currYearData,
              fill: false,
            },
            {
              label: this.years.prevYear,
              fill: false,
              backgroundColor: "#fff",
              borderColor: "#fff",
              //data: [40, 68, 86, 74, 56, 60, 87],
              //data: this.yearData.prevYearData
              data: this.$props.data.prevYearData
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          responsive: true,
          title: {
            display: false,
            text: "Sales Charts",
            fontColor: "white",
          },
          legend: {
            labels: {
              fontColor: "white",
            },
            align: "end",
            position: "bottom",
          },
          tooltips: {
            mode: "index",
            intersect: false,
          },
          hover: {
            mode: "nearest",
            intersect: true,
          },
          scales: {
            xAxes: [
              {
                ticks: {
                  fontColor: "rgba(255,255,255,.7)",
                },
                display: true,
                scaleLabel: {
                  display: false,
                  labelString: "Month",
                  fontColor: "white",
                },
                gridLines: {
                  display: false,
                  borderDash: [2],
                  borderDashOffset: [2],
                  color: "rgba(33, 37, 41, 0.3)",
                  zeroLineColor: "rgba(0, 0, 0, 0)",
                  zeroLineBorderDash: [2],
                  zeroLineBorderDashOffset: [2],
                },
              },
            ],
            yAxes: [
              {
                ticks: {
                  fontColor: "rgba(255,255,255,.7)",
                },
                display: true,
                scaleLabel: {
                  display: false,
                  labelString: "Value",
                  fontColor: "white",
                },
                gridLines: {
                  borderDash: [3],
                  borderDashOffset: [3],
                  drawBorder: false,
                  color: "rgba(255, 255, 255, 0.15)",
                  zeroLineColor: "rgba(33, 37, 41, 0)",
                  zeroLineBorderDash: [2],
                  zeroLineBorderDashOffset: [2],
                },
              },
            ],
          },
        },
      };
      var ctx = document.getElementById("line-chart").getContext("2d");
      window.myLine = new Chart(ctx, config);
    });
  },
};
</script>