<template>

  <body class="bg-primary p-5" :class="{ 'pointer-events-none': isLoading, 'brightness-50': isLoading }">
    <div v-if="isLoading" class="absolute w-full h-full">
      <Spinner />
    </div>
    <div v-if="!isLoading" class="kitchen">
      <button class="kitchen-controls" @click="moveOrders('left')">&laquo;</button>
      <div class="kitchen-orders" ref="ordersContainer">
        <transition-group name="fade" tag="div" class="orders-container">
          <div v-for="order in filteredOrders" :key="order.id" class="kitchen-ticket" :data-order-id="order.id">
            <div class="ticket-header">Order #{{ order.id }}</div>
            <ul class="ticket-items">
              <li v-for="item in orderItems[order.id]" :key="item">{{ item.name }}</li>
            </ul>
            <div class="ticket-actions">
              <button class="cancel-btn" @click="cancelOrder(order.id)">Cancel</button>
              <button class="ready-btn" @click="markReady(order.id)">Ready</button>
            </div>
          </div>
        </transition-group>
      </div>
      <button class="kitchen-controls" @click="moveOrders('right')">&raquo;</button>
    </div>
  </body>
</template>

<script>
import axios from 'axios';
import { LOCAL_BASE_URL, OrderStatus, PROD_BASE_URL } from '../../main';
import Spinner from "@/components/Loaders/Spinner.vue";

export default {
  components: { Spinner },
  data() {
    return {
      isLoading: false,
      orders: [],
      orderItems: {},
      currentPage: 0,
      pageSize: 4,
    };
  },
  mounted() {
    this.isLoading = true;
    this.fetchOrders();
    this.isLoading = false;
    this.startLiveReload()
    // this.refreshInterval = setInterval(this.fetchOrders, 5000);
  },
  // beforeUnmount() {
  //   clearInterval(this.refreshInterval);
  // },
  computed: {
    filteredOrders() {
      const start = this.currentPage * this.pageSize;
      const end = start + this.pageSize;
      return this.orders.slice(start, end);
    },
  },
  methods: {
    startLiveReload(initalDelay = 1000, proceedDelay = 1000){
      const self = this
      this.reloadTimeout = setTimeout(async function updateMenu (){
        self.fetchOrders()
        self.redirectTimeOut = setTimeout(() => updateMenu(), proceedDelay)
      }, initalDelay)
    },
    stopLiveReload(){
// Clear the timeouts if they are set
      if (this.reloadTimeout) {
          clearTimeout(this.reloadTimeout);
      }
      if (this.redirectTimeout) {
          clearTimeout(this.redirectTimeout);
      }
    },
    async fetchOrders() {
      try {
        const response = await axios.get(`${LOCAL_BASE_URL}/order/?status=0`);
        // this.orders = response.data.filter(order => order.status === OrderStatus.IN_PROGRESS);
        // console.log(response.data)
        this.orders = response.data
        let count = 0
        for (const order of this.orders) {
          if (count++ == 3) {
            this.isLoading = false;
          }
          this.orderItems[order.id] =  this.getItems(order.id);
        }
      } catch (error) {
        console.error("Error fetching orders:", error);
      }
      this.isLoading = false;
    },
    async markReady(orderID) {
      try {
        for(const menuItem of this.orderItems[orderID]) {
          console.log(menuItem)
          const response = await axios.get(`${PROD_BASE_URL}/menu_inventory/?menu_id=${menuItem.id}`)
          const inventoryItems = response.data
          console.log(inventoryItems)
          for(const inventoryItem of inventoryItems) {
            axios.get(`${PROD_BASE_URL}/inventory/${inventoryItem.inventory}/`)
            .then(response => {
              const currentStock = response.data.stock
              const newStock = currentStock - 1
              axios.patch(`${PROD_BASE_URL}/inventory/${inventoryItem.inventory}/`, {stock: newStock})
            });
          }
        }
        this.removeOrder(orderID);
        await axios.patch(`${PROD_BASE_URL}/order/${orderID}/`, { status: OrderStatus.COMPLETED });
      } catch (error) {
        console.error(`Error updating order status for ${orderID}: `, error);
      }
    },
    async cancelOrder(orderID) {
      try {
        this.removeOrder(orderID);
        await axios.patch(`${PROD_BASE_URL}/order/${orderID}/`, { status: OrderStatus.INCOMPLETE });
      } catch (error) {
        console.error(`Error updating order status for ${orderID}: `, error);
      }
    },

    async getItems(orderID) {
      const items = []
      try {
        const response = await axios.get(`${PROD_BASE_URL}/order_menu/?order_id=${orderID}`);
        for (let i = 0; i < response.data.length; i++) {
          const item = await axios.get(`${PROD_BASE_URL}/menu/${response.data[i].menu}/`)
          items.push(item.data.name)
        }
      } catch (error) {
        console.error(`Error getting items for ${orderID}: `, error);
      }
      console.log(items)
      return items
    },

    removeOrder(orderID) {
      const ticketIndex = this.orders.findIndex(order => order.id === orderID);
      if (ticketIndex !== -1) {
        this.orders.splice(ticketIndex, 1);
      }
    },
    moveOrders(direction) {
      if (direction === 'left' && this.currentPage > 0) {
        this.currentPage--;
      } else if (direction === 'right' && this.filteredOrders.length >= this.pageSize) {
        this.currentPage++;
      }
    },
  },
};
</script>

<style scoped>
.kitchen {
  padding-top: 25vh;
  display: flex;
  height: 75vh;
}

.kitchen-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 10px;
  color: white;
  font-size: 75px;
}

.kitchen-controls button {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.kitchen-orders {
  flex: 1;
  display: flex;
}

.orders-container {
  display: flex;
  width: 100%;
}

.kitchen-ticket {
  background-color: white;
  border-radius: 10px;
  margin: 10px;
  padding: 10px;
  width: 25%;
}

.ticket-header {
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 50px;
}

.ticket-items {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 25px;
  height: 80%;
}

.ticket-actions {
  display: flex;
  /* padding-top: 65%; */
  justify-content: space-between;
}

.ticket-actions button {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #ff6961;
  color: white;
  transition: background-color 0.3s ease;
}

.cancel-btn:hover {
  background-color: #e53935;
}

.ready-btn {
  background-color: #4caf50;
  color: white;
  transition: background-color 0.3s ease;
}

.ready-btn:hover {
  background-color: #388e3c;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-move {
  transition: transform 0.5s ease;
}
</style>