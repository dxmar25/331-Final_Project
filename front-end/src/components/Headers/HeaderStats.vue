<template>
  <!-- Header -->
  <div class="relative bg-red-400 md:pt-32 pb-32 pt-12">
    <div class="px-4 md:px-10 mx-auto w-full">
      <div>
        <!-- Card stats -->
        <div class="flex flex-wrap">
          <div class="w-full lg:w-6/12 xl:w-3/12 px-4">
            <card-stats
              v-if="loadorder"
              statSubtitle="NUMBER OF ORDERS TODAY"
              :statTitle="totalOrdertoday"
              :statArrow="orderstatarrow"
              :statPercent="percentOrderdiff"
              :statPercentColor="orderpercentcolor"
              statDescripiron="Since yesterday"
              statIconName="far fa-chart-bar"
              statIconColor="bg-red-500"
            />
          </div>
          <div class="w-full lg:w-6/12 xl:w-3/12 px-4">
            <card-stats
              v-if="loadorder"
              statSubtitle="AVERAGE SALES PER ORDER"
              :statTitle="`$${avgSaleOrder}`"
              :statArrow="avgstatarrow" 
              :statPercent="percentavgdiff"
              :statPercentColor="avgpercentcolor"
              statDescripiron="Since yesterday"
              statIconName="fas fa-chart-pie"
              statIconColor="bg-orange-500"
            />
          </div>
          <div class="w-full lg:w-6/12 xl:w-3/12 px-4">
            <card-stats
              v-if="loadorder"
              statSubtitle="TOTAL SALES TODAY"
              :statTitle="`$${totalSalestoday}`"
              :statArrow="salesstatarrow"
              :statPercent="percentSalesdiff"
              :statPercentColor="salespercentcolor"
              statDescripiron="Since yesterday"
              statIconName="fas fa-users"
              statIconColor="bg-pink-500"
            />
          </div>
          <div class="w-full lg:w-6/12 xl:w-3/12 px-4">
            <card-stats
              v-if="loadinven"
              statSubtitle="TOTAL INDIVIDUAL ITEMS UNDERSTOCKED"
              :statTitle="totalInventoryunder"
              :statArrow="inventorystatarrow"
              :statPercent="percentInventorydiff"
              :statPercentColor="inventorypercentcolor"
              statDescripiron="Total"
              statIconName="fas fa-percent"
              statIconColor="bg-emerald-500"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CardStats from "@/components/Cards/CardStats.vue";
import axios from 'axios'

export default {
  components: {
    CardStats,
  },
  data() {
    return {
      totalOrdertoday: 0,
      totalOrderyest: 0,
      percentOrderdiff: 0,
      orderstatarrow: "",
      orderpercentcolor: "",

      totalSalestoday: 0,
      totalSalesyest: 0,
      percentSalesdiff: 0,
      salesstatarrow: "",
      salespercentcolor: "",

      totalInventory: 0,
      totalInventoryunder: 0,
      percentInventorydiff: 0,
      inventorystatarrow: "",
      inventorypercentcolor: "",

      avgSaleOrder: 0,
      avgSaleOrderyest: 0,
      percentavgdiff: 0,
      avgstatarrow: "",
      avgpercentcolor: "",

      dates: {
        currYear: new Date().getFullYear(),
        currMonth: new Date().getMonth(),
        currDay: new Date().getDay(),
      },

      loadorder: false,
      loadinven: false,

    };
  },
  methods: {
    async fetchorderData() {
      try {
        //const response = await axios.get('https://project-3-full-stack-agile-web-902-team-3-jctc.onrender.com/order');
        const PROD_BASE_URL = 'https://project-3-full-stack-agile-web-902-team-3-jctc.onrender.com';
        const today = new Date().toISOString().split('T')[0];
        const yesterday = new Date(Date.now() - 864e5).toISOString().split('T')[0];
        
        const response = await axios.get(`${PROD_BASE_URL}/order/?timestamp__gte=${yesterday}&timestamp__lt=${today}&ordering=-timestamp`);
        response.data.forEach(({ total, timestamp, status }) => {
          const year = parseInt(timestamp.split('-')[0]);
          const month = parseInt(timestamp.split('-')[1]);
          const day = parseInt(timestamp.split('-')[2]);

          
          if (year === this.dates.currYear && month === this.dates.currMonth && status === 1) {
            if (day === this.dates.currDay) {
              this.totalOrdertoday += 1;
              this.totalSalestoday += total;
            }
            else if (day === this.dates.currDay-1) {
              this.totalOrderyest += 1;
              this.totalSalesyest += total;
            }
          }
        });

        if (this.totalOrderyest === 0) this.totalOrderyest += 1;
        this.percentOrderdiff = (((this.totalOrdertoday - this.totalOrderyest) / this.totalOrderyest) * 100).toFixed(2);
        this.orderstatarrow = this.percentOrderdiff >= 0 ? "up" : "down";
        this.orderpercentcolor = this.orderstatarrow === "up" ? "text-emerald-500" : "text-red-500";
        this.totalOrderstoday = this.totalOrdertoday.toFixed(2);

        if (this.totalSalesyest === 0) this.totalSalesyest += 1;
        this.percentSalesdiff = (((this.totalSalestoday - this.totalSalesyest) / this.totalSalesyest) * 100).toFixed(2);
        this.salesstatarrow = this.percentSalesdiff >= 0 ? "up" : "down";
        this.salespercentcolor = this.salesstatarrow === "up" ? "text-emerald-500" : "text-red-500";
        this.totalSalestoday = this.totalSalestoday.toFixed(2);

        if (this.avgSaleOrderyest === 0) this.avgSaleOrderyest += 1;
        if (this.totalOrdertoday === 0) this.totalOrdertoday += 1;
        if (this.totalOrderyest === 0) this.totalOrdertoday += 1;
        this.avgSaleOrder = (this.totalSalestoday / this.totalOrdertoday).toFixed(2);
        this.avgSaleOrderyest = this.totalSalesyest / this.totalOrderyest;
        this.percentavgdiff = (((this.avgSaleOrder - this.avgSaleOrderyest) / this.avgSaleOrderyest) * 100).toFixed(2);
        this.avgstatarrow = this.percentavgdiff >= 0 ? "up" : "down";
        this.avgpercentcolor = this.avgstatarrow === "up" ? "text-emerald-500" : "text-red-500";

        this.loadorder = true;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },

    async fetchinventoryData() {
      try {
        const response = await axios.get('https://project-3-full-stack-agile-web-902-team-3-jctc.onrender.com/inventory');
        response.data.forEach(({ stock, reorder_level }) => {
          this.totalInventory += 1;
          if (stock <= reorder_level) {
            this.totalInventoryunder += 1;
          }
        });

        if (this.totalInventory === 0) this.totalInventory += 1;
        this.percentInventorydiff= ((this.totalInventoryunder / this.totalInventory) * 100).toFixed(2);
        this.inventorystatarrow = this.percentInventorydiff > 0 ? "down" : "up";
        this.inventorypercentcolor = this.inventorystatarrow === "up" ? "text-emerald-500" : "text-red-500";
        this.totalInventoryunder = this.totalInventoryunder.toFixed(2);

        this.loadinven = true;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
  mounted() {
    this.fetchorderData();
    this.fetchinventoryData();
  },
};
</script>
