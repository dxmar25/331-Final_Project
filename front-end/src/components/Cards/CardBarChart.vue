<template>
  <div
    class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded"
  >
    <div class="rounded-t mb-0 px-4 py-3 bg-transparent">
      <div class="flex flex-wrap items-center">
        <div class="relative w-full max-w-full flex-grow flex-1">
          <h6 class="uppercase text-blueGray-400 mb-1 text-xs font-semibold">
            Overview
          </h6>
          <h2 class="text-blueGray-700 text-xl font-semibold">
            Total Orders
          </h2>
        </div>
      </div>
    </div>
    <div class="p-4 flex-auto">
      <div class="relative h-350-px">
        <canvas id="bar-chart"></canvas>
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
  //     orderData.data.forEach(({ timestamp, status }) => {
  //       const month = timestamp.split('-')[1];
  //       const year = timestamp.split('-')[0];
  //       if (year == this.years.currYear && status == 0) {
  //         this.yearData.currYearData[month-1] += 1;
  //       }
  //       else if (year == this.years.prevYear && status == 0) {
  //         this.yearData.prevYearData[month-1] += 1;
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
      let config = {
        type: "bar",
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
              backgroundColor: "#ed64a6",
              borderColor: "#ed64a6",
              //data: [30, 78, 56, 34, 100, 45, 13],
              //data: this.yearData.currYearData,
              data: this.$props.data.currYearData,
              fill: false,
              barThickness: 8,
            },
            {
              label: this.years.prevYear,
              fill: false,
              backgroundColor: "#4c51bf",
              borderColor: "#4c51bf",
              //data: [27, 68, 86, 74, 10, 4, 87],
              //data: this.yearData.prevYearData,
              data: this.$props.data.prevYearData,
              barThickness: 8,
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          responsive: true,
          title: {
            display: false,
            text: "Orders Chart",
          },
          tooltips: {
            mode: "index",
            intersect: false,
          },
          hover: {
            mode: "nearest",
            intersect: true,
          },
          legend: {
            labels: {
              fontColor: "rgba(0,0,0,.4)",
            },
            align: "end",
            position: "bottom",
          },
          scales: {
            xAxes: [
              {
                display: false,
                scaleLabel: {
                  display: true,
                  labelString: "Month",
                },
                gridLines: {
                  borderDash: [2],
                  borderDashOffset: [2],
                  color: "rgba(33, 37, 41, 0.3)",
                  zeroLineColor: "rgba(33, 37, 41, 0.3)",
                  zeroLineBorderDash: [2],
                  zeroLineBorderDashOffset: [2],
                },
              },
            ],
            yAxes: [
              {
                display: true,
                scaleLabel: {
                  display: false,
                  labelString: "Value",
                },
                gridLines: {
                  borderDash: [2],
                  drawBorder: false,
                  borderDashOffset: [2],
                  color: "rgba(33, 37, 41, 0.2)",
                  zeroLineColor: "rgba(33, 37, 41, 0.15)",
                  zeroLineBorderDash: [2],
                  zeroLineBorderDashOffset: [2],
                },
              },
            ],
          },
        },
      };
      let ctx = document.getElementById("bar-chart").getContext("2d");
      window.myBar = new Chart(ctx, config);
    });
  },
};
</script>