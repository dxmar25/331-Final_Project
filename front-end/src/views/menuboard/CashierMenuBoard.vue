<!-- Cashier Menu Board -> /cashier-order -->

<template>
  <div class=" bg-primary h-screen grid grid-cols-4 grid-rows-6 p-4 relative"
    :class="{ 'pointer-events-none': isLoading, 'brightness-50': isLoading }">

    <div v-if="isLoading" class="absolute w-full h-full z-50">
      <Spinner />
    </div>
    <!-- Log modal -->
    <div :class="{ '!w-0': !isOpenLogging }" class="absolute">
      <Modal :show="isOpenLogging" @close="closeLog" size="large">
        <template v-slot:header>
          <h1 class=" font-bold text-xl underline underline-offset-1"> Order Log</h1>
        </template>
        <template v-slot:body>
          <ul class="flex flex-col gap-4">
            <li v-for="({ details, timeAgo }) in orderLog">{{ details }} <em> ~ {{ timeAgo }}</em>
            </li>
          </ul>
        </template>
        <template v-slot:footer />
      </Modal>
    </div>
    <!-- Edit order modal  -->
    <div :class="{ '!w-0': !isOpenOrderEdit }" class="absolute">
      <Modal :show="isOpenOrderEdit" @close="closeEdit" size="small">
        <template v-slot:header>
          <h1 class=" font-bold text-xl underline underline-offset-1"> Active/Pending Orders Log</h1>
        </template>
        <template v-slot:body>
          <ul class="flex flex-col gap-4">
            <li class="flex items-center" v-for="({ id, details, timeAgo }) in activeOrders">{{ details
              }}
              <em> ~ {{ timeAgo
                }}</em>
              <div class="flex ml-auto">
                <PrimaryButton @click="loadOldOrders(id)" size="small">Edit</PrimaryButton>
              </div>
            </li>
          </ul>
        </template>
        <template v-slot:footer />
      </Modal>
    </div>
    <!-- Receipt -->
    <div class="bg-[#f56465]  row-span-6 col-span-1 relative mr-2 z-10 overflow-y-scroll pb-20 text-white">
      <div v-for="(item, index) in currentOrder" class="p-2">
        <div class="flex justify-between items-center">
          <span class="text-lg "><b>{{ item.name }}</b> ({{ formatPrice(item.price) }}ea)</span>
          <div class="flex  font-extrabold text-black">
            <button class="w-8  bg-[#E1E8EE]" @click="subtractOneQuantity(index)" type="button" name="button" >
              -
            </button>
            <input class="text-center text-sm w-14" maxlength="2" type="text" @keyup="setQuantity(index, $event)" :value="item.quantity"
            >
            <button class="w-8  bg-[#E1E8EE]" @click="addOneQuantity(index)" type="button" name="button" :class="{ 'pointer-events-none': !item.isAvailable, 'brightness-50': !item.isAvailable}">
              +
            </button>
          </div>
        </div>

      </div>

      <span class="p-2 fixed bottom-4 text-[30px] font-bold backdrop-blur-xl flex">Total: {{
        formatPrice(calculateTotal)
      }}

      </span>
    </div>
    <!-- NavBar -->
    <div class="w-full col-span-3 max-h-12 fixed right-0 pr-6">
      <ul class="flex justify-end divide-x-2 !text-white">
        <li class="cursor-pointer hover:underline-offset-2 hover:underline text-lg px-2 text-white"><a
            @click="openLog">Order
            Log</a>
        </li>
        <li class="cursor-pointer hover:underline-offset-2 hover:underline text-lg px-2 text-white"><a
            @click="openEdit">Active
            Orders</a></li>
        <li class="cursor-pointer hover:underline-offset-2 hover:underline text-lg px-2 "><a
            @click="$router.push('/kitchen')">Kitchen</a></li>
      </ul>

    </div>

    <!-- Category -->
    <div class=" row-span-1 col-span-3 flex justify-between gap-3 pt-10">
      <PrimaryButton @click="switchCategory(value)" class="flex-1 justify-center items-center flex-col text-center"
        v-for="(value, key) in categories" :key="key">
        <div class="w-12">
          <img :src="categoryImages[key]" alt="">
        </div>
        <span class="font-bold text-nowrap
        ">
          {{ value.charAt(0).toUpperCase() + value.slice(1) }}
        </span>
      </PrimaryButton>

    </div>
    <!-- Menu items -->
    <div class="flex flex-wrap items-start col-span-3 row-span-4 gap-5 pt-5">
      <!-- :class="{ 'pointer-events-none': !item.isAvailable, 'brightness-50': !item.isAvailable}" -->
      <PrimaryButton @click="addToOrder({ ...item, name, category: activeCategory, quantity: 1 })" class="shadow-lg" :class="{ 'pointer-events-none': !item.isAvailable, 'brightness-50': !item.isAvailable}"  
        v-for="(item, name) in (menu[findBestMatchedKey(activeCategory, menu)])">
        {{name}} ({{formatPrice(item.price)}})
        <!-- {{ name }} ({{ formatPrice(item.price) }}) -->
      </PrimaryButton>
    </div>
    <!-- Submit Button -->
    <div class="row-span-1 col-span-3 relative flex gap-2
    ">
      <div class="absolute bottom-0 right-0 flex gap-2">
        <PrimaryButton class="bg-white !text-primary"
          :class="{ 'pointer-events-none': currentOrder.length == 0, 'brightness-50': currentOrder.length == 0 }"
          @click="clearOrder">Clear Order</PrimaryButton>
        <PrimaryButton
          :class="{ 'pointer-events-none': isOrderValid && currentOrder.length == 0 && !editOrderId, 'brightness-50': currentOrder.length == 0 && !editOrderId && isOrderValid }"
          @click="submitOrder" class=" bg-white !text-primary">{{ editOrderId ? "Update" :
            "Submit"
          }}
        </PrimaryButton>

      </div>


      <PrimaryButton :class="{ 'pointer-events-none': editOrderId == null, 'brightness-50': editOrderId == null }"
        @click="exitEditOrder" class="absolute  bottom-0 bg-white !text-primary">Exit Order Edit
      </PrimaryButton>
    </div>
  </div>
</template>

<script>
import PrimaryButton from "@/components/Buttons/PrimaryButton.vue";
import burger from "@/assets/burger.png"
import basket from "@/assets/basket.png"
import beverage from "@/assets/beverage.png"
import sandwich from "@/assets/sandwich.png"
import sauce from "@/assets/sauce.png"
import shake from "@/assets/shake.png"
import side from "@/assets/side.png"
import axios from 'axios'
import Spinner from "@/components/Loaders/Spinner.vue";
import Modal from "@/components/Modal/Modal.vue";
import { getCookie } from "../../cookies/cookies";
import { PROD_BASE_URL, OrderStatus, LOCAL_BASE_URL, ReverseMenuCategories } from "../../main";

export default {
  components: {
    PrimaryButton,
    Spinner,
    Modal
  },
  computed: {
    calculateTotal() {
      return this.currentOrder.reduce((total, item) => total + item.price * item.quantity, 0);
    },
  },

  data() {
    return {
      MAX_ORDER_LIMIT: 200,

      menu: {
      },

      idToMenu: {
      },
      surgeMultiplier: {},
      categories: {
        BURGERS: "burgers",
        BEVERAGES: "beverages",
        SANDWICHES: "sandwiches",
        SAUCES: "sauces",
        "SHAKES N SWEETS": "shakes n sweets",
        SIDES: "sides",
        BASKETS: "baskets"
      },
      categoryImages: {
        BURGERS: burger,
        BASKETS: basket,
        BEVERAGES: beverage,
        SANDWICHES: sandwich,
        SAUCES: sauce,


        "SHAKES N SWEETS": shake,
        SIDES: side
      },
      currentOrderId: null,
      currentOrder: [], //{name, price, quantity}
      activeCategory: "BURGERS",
      isLoading: false,
      editOrderId: null,
      isOpenLogging: false,
      isOpenOrderEdit: false,
      isOrderValid: true,
      orderLog: [],
      activeOrders: [],
      redirectTimeOut: null,
      reloadTimeout: null

    };
  },
  methods: {
    async loadInit(){
      this.isLoading = true
      this.loadSurgePrices();
      await this.loadMenu();
      await this.setMenuItemAvailable()
      this.isLoading = false;
    },
    async loadSurgePrices(){
      const surgeData = (await axios.get(`${LOCAL_BASE_URL}/weather/`)).data.surge
      this.surgeMultiplier = surgeData;
    },
    async loadMenu() {

      const menuData = (await axios.get(`${LOCAL_BASE_URL}/menu`)).data
      const newMenu = {}
      menuData.forEach(({ id, name, price, category }) => {
        this.idToMenu[id] = { name, price, category }
        const categoryStr = ReverseMenuCategories[category]
        const newSurgedPrice = price * this.surgeMultiplier[this.findBestMatchedKey(categoryStr,
                    this.surgeMultiplier)] || price

        let availability = this.menu[categoryStr]?.[name]?.isAvailable
        if(!newMenu[categoryStr]){
          newMenu[categoryStr] = {}
        }
        if(availability == undefined){
          availability = true
        }
        newMenu[categoryStr][name] = {price: newSurgedPrice, id, isAvailable: availability}

    });
    this.menu = newMenu
    // this.$forceUpdate()
    },
    async loadLog() {
      this.isLoading = true;
      const limit = 25;
      const offset = 0;
      const logData = (await axios.get(`${LOCAL_BASE_URL}/order/?limit=${limit}&offset=${offset}&ordering=-timestamp`)).data;
      //extract log details for ui
      this.orderLog = logData.map((entry) => {
        let details = `Order#${entry.id} (${this.formatPrice(entry.total)}) was `
        switch (entry.status) {
          case OrderStatus.IN_PROGRESS:
            details += "created or edited by "
            break;
          case OrderStatus.COMPLETED: //
            details += "completed by "
            break;
          case OrderStatus.INCOMPLETE:
            details += "marked incomplete (refunded) by "
            break;
          case OrderStatus.DELETED:
            details += "deleted by "
            break;
        }

        details += (entry.employee == getCookie("id")) ? `YOU (#${entry.employee})` : `Employee#${entry.employee}`
        const timeAgo = `${this.calculateTimeAgoString(entry.timestamp)} ago`
        return { id: entry.id, details, timeAgo }
      });
      this.isLoading = false;
    },
    async loadActiveOrders() {
      this.isLoading = true;
      const limit = 25;
      const offset = 0;
      const inProgressOrders = (await axios.get(`${LOCAL_BASE_URL}/order/?limit=${limit}&offset=${offset}&status=0&ordering=-timestamp`)).data;
      this.activeOrders = inProgressOrders.map((entry) => {
        let details = `Order#${entry.id} `
        const timeAgo = `${this.calculateTimeAgoString(entry.timestamp)} ago`
        return { id: entry.id, details, timeAgo }
      })
      this.isLoading = false
    },
    async loadOldOrders(orderId) {
      this.isLoading = true;
      this.editOrderId = orderId;

      const oldOrder = (await axios.get(`${LOCAL_BASE_URL}/order_menu/?order_id=${orderId}`)).data; //production url doesn't work with order_id
      const sameOrderGroup = {};

      // Group items by order and menu numbers
      oldOrder.forEach(item => {
        const key = `${item.order}-${item.menu}`;
        if (!sameOrderGroup[key]) {
          sameOrderGroup[key] = item;
        } else {
          sameOrderGroup[key].quantity += item.quantity;
        }
      });
      this.currentOrder = Object.values(sameOrderGroup).map(({ menu, quantity }) => {
        const menuData = this.idToMenu[menu]
        return { id: menu, quantity, name: menuData.name, price: menuData.price }
      })
      this.closeEdit()
      this.isLoading = false
    },
    findBestMatchedKey(searchKey, object) {
      let bestKey = null;
      for (const key of Object.keys(object)) {
        const normalizedSearchKey = searchKey.toLowerCase().replace(/\s/g, '')
        const normalizeKey = key.toLowerCase().replace(/\s/g, '')
        if (normalizeKey == normalizedSearchKey) {
          return key
        }
        if (normalizeKey.includes(normalizedSearchKey) || normalizedSearchKey.includes(normalizeKey)) {
          bestKey = key;
        }

      }
      return bestKey
    },
    exitEditOrder() {
      this.editOrderId = null;
      this.currentOrder = []
    },
    calculateTimeAgoString(timestamp) {
      const currentTime = new Date();
      const previousTime = new Date(timestamp);
      const timeDifference = currentTime - previousTime;
      const secAgo = Math.floor(timeDifference / 1000)
      const minutesAgo = Math.floor(timeDifference / (1000 * 60));
      const hoursAgo = Math.floor(minutesAgo / 60);
      const daysAgo = Math.floor(hoursAgo / 24);

      if (daysAgo >= 1) return daysAgo + " days"
      if (hoursAgo >= 1) return hoursAgo + " hrs"
      if (minutesAgo >= 1) return minutesAgo + " mins";
      return secAgo + " secs"
    },
    openLog() {
      this.isOpenLogging = true;
      this.loadLog();
    },
    closeLog() {
      this.isOpenLogging = false;
    },
    openEdit() {
      this.isOpenOrderEdit = true;
      this.loadActiveOrders()
    },
    closeEdit() {
      this.isOpenOrderEdit = false;
    },
    addToOrder(newItem) { //note this is proxy
      const existingItemIndex = this.currentOrder.findIndex(item => item.name === newItem.name);
      if (existingItemIndex !== -1) {
        this.currentOrder[existingItemIndex].quantity += newItem.quantity;
      } else {
        this.currentOrder.push(newItem);
      }
    },
    clearOrder() {
      this.currentOrder = []
    },
    async submitOrder() {

      this.isLoading = true

      try {

        const menuAvailability = await this.setMenuItemAvailable()
        if(!menuAvailability) throw error;
        const insufficientIds = menuAvailability.map((item) => item.id)
        const insufficientItemInOrder = this.currentOrder.map((item) => {
          const index = insufficientIds.indexOf(item.id)
          if(index == -1) return null;
          const quantity = menuAvailability[index]?.insufficient_inventory_quantity
          if (index != -1 && quantity < 0){
            return {name: item.name, deficit: quantity}
          }
        }).filter(item => item !== undefined && item !== null);
        if(insufficientItemInOrder.length){
          const formattedInsufficientOrder =  insufficientItemInOrder?.map(item => `${item.name} (${item.deficit})`);
          alert(`Insufficient inventory for item: ${formattedInsufficientOrder}`);
          this.isLoading = false
          return;
        }
       
        // return
        // throw error
        const orderData = { status: this.calculateTotal == 0 ? 2 : 0, total: this.calculateTotal, timestamp: new Date().toISOString(), employee: getCookie("id") }
        
        
        if (this.editOrderId) {
          await axios.put(`${LOCAL_BASE_URL}/order/${this.editOrderId}/`, orderData)
          await axios.delete(`${LOCAL_BASE_URL}/order_menu/?order_id=${this.editOrderId}`) //BUG: Production url doesn't work order_id
          for (const item of this.currentOrder) {
            const orderMenuData = { quantity: item.quantity, order: this.editOrderId, menu: item.id }
            await axios.post(`${LOCAL_BASE_URL}/order_menu/`, orderMenuData)
          }
        }
        else {
          const orderResponse = await axios.post(`${LOCAL_BASE_URL}/order/`, orderData)
          for (const item of this.currentOrder) {
            const orderMenuData = { quantity: item.quantity, order: orderResponse.data.id, menu: item.id }
            await axios.post(`${LOCAL_BASE_URL}/order_menu/`, orderMenuData)
          }
        }
        this.editOrderId = null


        this.currentOrder = [];

      } catch (error) {
        console.log(error);
        alert("Sorry, something went wrong with our server.")
      }
      this.isLoading = false;
    },
    // setting menu item availability
    async setMenuItemAvailable() {
      const url = `${LOCAL_BASE_URL}/menu_inventory/check_inventory/`;
      const menuItems = Object.values(this.menu[this.findBestMatchedKey(this.activeCategory, this.menu)] || [])
      const menuIds = menuItems.map(menuItem => menuItem.id)

      const deductions = this.currentOrder?.map(order => ({id: order.id, quantity: order.quantity}))
    
      const requestData = {
        menu_ids: menuIds,
        deductions: deductions,
      };
      const response =  await axios.post(url, requestData);

      if(response.data.insufficient_items){
          const bestKey = this.findBestMatchedKey(this.activeCategory, this.menu)
          const insufficient_ids = response.data.insufficient_items.map((item) => item.id)
          for(const [key, value] of Object.entries(this.menu[bestKey])){
            const {id, price} = value
            this.menu[bestKey][key].isAvailable = !insufficient_ids.includes(id)
            this.currentOrder.forEach((order) => order.isAvailable = !insufficient_ids.includes(order.id))
          }
          return response.data.insufficient_items
        }
        return null

    },
    switchCategory(category) {
      this.activeCategory = category
    },
    addOneQuantity(index) {
      this.currentOrder[index].quantity++
      if(this.currentOrder[index].quantity >= 100){
        this.currentOrder[index].quantity = 99;
      }
    },
    subtractOneQuantity(index) {
      this.currentOrder[index].quantity--;
      if (this.currentOrder[index].quantity <= 0) {
        this.currentOrder.splice(index, 1)
      }
    },
    setQuantity(index, event) {
      const newQuantity = event.target.value
      const refinedNewQuantity = newQuantity.toString().replace(/\D+/g, '').substring(0,2)

      this.currentOrder[index].quantity = parseInt(refinedNewQuantity) || 0
      event.target.value = refinedNewQuantity

    },
    formatPrice(price) {
      const USDFormatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      });
      return USDFormatter.format(price)
    },
    startLiveReload(initalDelay = 2000, proceedDelay = 1000){
      const self = this
      this.reloadTimeout = setTimeout(async function updateMenu (){
         await self.loadMenu()
         await self.setMenuItemAvailable()
        self.redirectTimeOut = setTimeout(() => updateMenu(), proceedDelay)
      }, initalDelay)
    },
  stopLiveReload() {
    // Clear the timeouts if they are set
    if (this.reloadTimeout) {
        clearTimeout(this.reloadTimeout);
    }
    if (this.redirectTimeout) {
        clearTimeout(this.redirectTimeout);
    }
},},
  async mounted(){
    await this.loadInit()
    this.startLiveReload()
  },
  beforeRouteLeave(to, from, next){
    this.stopLiveReload()
    next()
  }
  
};
</script>

