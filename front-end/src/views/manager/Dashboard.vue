<script>
import CardLineChart from "@/components/Cards/CardLineChart.vue";
import CardBarChart from "@/components/Cards/CardBarChart.vue";
import axios from 'axios'
export default {
  name: "dashboard-page",
  components: {
    CardLineChart,
    CardBarChart,
  },
  data() {
    return {
      loaded: false,

      lineChartData: {
        currYearData: Array(12).fill(0),
        prevYearData: Array(12).fill(0),
      },
      barChartData: {
        currYearData: Array(12).fill(0),
        prevYearData: Array(12).fill(0),
      },
      years: {
        currYear: new Date().getFullYear(),
        prevYear: new Date().getFullYear()-1,
      },
    };
  },
  methods: {
    async fetchData() {
      try {
        const cachedData = JSON.parse(localStorage.getItem('dashboardData'));
        const cacheExpiration = 22 * 60 * 60 * 1000; // 1 day in milliseconds
        const now = new Date().getTime();

        if (cachedData && (now - cachedData.lastFetched) < cacheExpiration) {
          this.lineChartData = cachedData.lineChartData;
          this.barChartData = cachedData.barChartData;
          this.loaded = true;
        } else {
          const orderData = await axios.get('https://project-3-full-stack-agile-web-902-team-3-jctc.onrender.com/order');
          this.processOrderData(orderData.data);
          localStorage.setItem('dashboardData', JSON.stringify({
            lineChartData: this.lineChartData,
            barChartData: this.barChartData,
            lastFetched: now
          }));
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    processOrderData(orderData) {
      orderData.forEach(({ total, timestamp, status }) => {
        const year = parseInt(timestamp.split('-')[0]);
        const month = parseInt(timestamp.split('-')[1]);
        if (year === this.years.currYear && status === 1) {
          this.lineChartData.currYearData[month-1] += total;
          this.barChartData.currYearData[month-1] += 1;
        } else if (year === this.years.prevYear && status === 1) {
          this.lineChartData.prevYearData[month-1] += total;
          this.barChartData.prevYearData[month-1] += 1;
        }
      });

      this.lineChartData.currYearData = this.lineChartData.currYearData.map(value => parseFloat(value.toFixed(2)));
      this.lineChartData.prevYearData = this.lineChartData.prevYearData.map(value => parseFloat(value.toFixed(2)));
      this.barChartData.currYearData = this.barChartData.currYearData.map(value => parseFloat(value.toFixed(2)));
      this.barChartData.prevYearData = this.barChartData.prevYearData.map(value => parseFloat(value.toFixed(2)));
      this.loaded = true;
    }
  },
  mounted() {
    this.fetchData();
  },
};
</script>


<template>
  <div>
    <div class="flex flex-wrap">
      <div class="w-full xl:w-8/12 mb-12 xl:mb-0 px-4">
        <CardLineChart v-if="loaded" :data="lineChartData" />
      </div>
      <div class="w-full xl:w-4/12 px-4">
        <CardBarChart v-if="loaded" :data="barChartData" />
      </div>
    </div>
  </div>
</template>