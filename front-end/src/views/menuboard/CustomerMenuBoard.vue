<template>
  <body class="bg-primary p-5" :class="{ 'pointer-events-none': isSubmitting, 'brightness-50': isSubmitting }">
    <div v-if="isSubmitting" class="absolute w-full h-full">
      <Spinner />
    </div>
    <div class="bg-primary p- 5">

      <div class="tab">
        
        <button class="image-button" @click="hideImages = !hideImages" tabindex="0" @focus="handleFocus($event)"
          @blur="handleBlur($event)">
        {{ hideImages ? 'Show Images' : 'Hide Images' }}
        </button>
        <button v-for="(id, categoryName) in MenuCategories" :key="id" @click="currentCategory = id" 
          :class="{ 'active': currentCategory === id }" tabindex="0" @focus="handleFocus($event)"
          @blur="handleBlur($event)">
          {{ categoryName.charAt(0).toUpperCase() + categoryName.slice(1).toLowerCase() }}
        </button>
        <button class="cart-button" @click="showCart = !showCart" tabindex="0" @focus="handleFocus($event)"
          @blur="handleBlur($event)">
          Cart ({{ cartItems.length }})
        </button>
      </div>

      <div class="menu-container">
        <div v-for="item in filteredMenuItems" :key="item.id" class="menu-item">
          <img :class="{ 'hidden' : hideImages }" :src=item.image alt="Menu Item Image">
          <div class="item-details">
            <h3>{{ item.name }}</h3>
            <p class="price">{{ formatPrice(item.price) }}</p>
            <button class="add-button" @click="addToCart(item)">Add to Order</button>
            <div class="divider"></div>
          </div>
        </div>
      </div>

      <div class="cart-modal" v-if="showCart">
        <div class="modal-content">
          <span class="close" @click="showCart = false">Close Cart</span>
          <br>
          <br>
          <br>
          <h2>Shopping Cart</h2>
          <ul>
            <li v-for="(item, index) in cartItems" :key="index" class="cart-item">
              <div class="cart-item-details">
                <span>{{ item.name }}</span>
                <span>{{ formatPrice(item.price) }}</span>
              </div>
              <button class="remove-button" @click="removeFromCart(index)">Remove</button>
            </li>
          </ul>
          <div class="cart-totals">
            <div class="cart-total">
              <span>Weather Charge:</span>
              <span>{{ formatPrice(calculateSurgeAdded) }}</span>
            </div>
            <div class="cart-total">
              <span>Total:</span>
              <span>{{ formatPrice(calculateTotal) }}</span>
            </div>
          </div>
          <div class="payment-options">
            <h3>Payment Options:</h3>
            <button class="payment-option" @click="showPaymentModal('retail')">Retail Swipe</button>
            <button class="payment-option" @click="showPaymentModal('credit')">Credit Card</button>
            <button class="payment-option" @click="showPaymentModal('cash')">Cash</button>
          </div>
        </div>
      </div>

      <div class="payment-modal" v-if="paymentModal">
        <div class="modal-content">
          <span class="close" @click="closePaymentModal">&times;</span>
          <div v-if="paymentType === 'retail'">
            <h3>Retail Swipe Payment</h3>
            <p>Please swipe your card at the terminal.</p>
            <button @click="checkout" class="submit-button">Submit Order</button>
          </div>
          <div v-if="paymentType === 'credit'">
            <h3>Credit Card Payment</h3>
            <form @submit.prevent="checkout" class="credit-card-form">
              <div class="form-group">
                <label for="cardNumber">Card Number:</label>
                <input type="text" id="cardNumber" v-model="formattedCardNumber" maxlength="16" required>
              </div>
              <div class="form-group">
                <label for="expirationDate">Expiration Date:</label>
                <input type="text" id="expirationDate" v-model="expirationDate" placeholder="MM/YY" maxlength="5" required>
              </div>
              <div class="form-group">
                <label for="cvv">CVV:</label>
                <input type="text" id="cvv" v-model="cvv" maxlength="3" required>
              </div>
              <button type="submit" class="submit-button">Submit Order</button>
            </form>
          </div>
          <div v-if="paymentType === 'cash'">
            <h3>Cash Payment</h3>
            <p>Please see the counter to pay with cash.</p>
            <button @click="checkout" class="submit-button">Submit Order</button>
          </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
import axios from 'axios';
import { getCookie } from "../../cookies/cookies";
import { MenuCategories, PROD_BASE_URL, LOCAL_BASE_URL } from '../../main';
import Spinner from "@/components/Loaders/Spinner.vue";

export default {

  components: { Spinner },
  data() {
    return {
      MenuCategories,
      menuItems: [],
      ingredients: [],
      currentCategory: MenuCategories.BURGERS,
      showCart: false,
      showEdit: false,
      cartItems: [],
      isSubmitting: false,
      redirectTimeOut: null,
      reloadTimeout: null,
      weather: {
        temperature: null,
        icon: '',
        condition: '',
        surge: {
          Burgers: 1.0, // set this to 1.0 just to put a value, in the weather.py the default is 1.1
          Baskets: 1.0,
          'Shakes n Sweets': 1.0,
          Sandwiches: 1.0,
          Beverages: 1.0,
          Sides: 1.0,
          Sauces: 1.0
        },
      },
      paymentModal: false,
      paymentType: null,
      creditCardNumber: '',
      expirationDate: '',
      cvv: '',
      hideImages: false,
    }
  },
  created() {
    this.isSubmitting = true;
    this.fetchMenuItems();
    this.fetchWeather();
    this.isSubmitting = false;
  },
  computed: {
    
    calculateSurgeAdded() {
      const totalWithoutSurge = this.cartItems.reduce((total, item) => total + item.price, 0);
      const totalWithSurge = this.calculateTotal;
      return totalWithSurge - totalWithoutSurge;
    },
    calculateTotal() {
      const surgeMultiplier = this.weather.surge[this.currentCategory] || 1.1;
      return this.cartItems.reduce((total, item) => total + (item.price * surgeMultiplier), 0);
    },
    filteredMenuItems() {
      if (this.currentCategory == MenuCategories.COMBOS) {
        return this.menuItems.filter(item => item.name.includes('Combo'))
      }
      if(this.currentCategory == MenuCategories.SEASONAL) {
        const today = new Date();
        const first = new Date("2024-01-01T00:00:00Z");
        const last = new Date("2024-12-31T00:00:00Z");
        const filteredItems = this.menuItems.filter(item => new Date(item.season_end) > today && new Date(item.season_start) < today);
        return filteredItems.filter(
          item => 
          item.season_start != (first.toISOString().slice(0, -5) + 'Z') && 
          item.season_end != last.toISOString().slice(0,-5) + 'Z');
      }
      else {
        return this.menuItems.filter(item => item.category == this.currentCategory && !item.name.includes('Combo'));
      }
    },
  },
  methods: {
    handleFocus(event) {
      //event.target.style.boxShadow = '0 0 0 4px rgba(59, 130, 246, 0.75)';
    },
    handleBlur(event) {
      //event.target.style.boxShadow = '';
    },
    
    async fetchMenuItems() {
      await axios.get(`${LOCAL_BASE_URL}/menu`)
        .then(response => {
          console.log(response.data)
          this.menuItems = response.data;
        })
        .catch(error => {
          console.error('Error fetching menu items:', error);
        });
    },
    fetchWeather() {
      axios.get(`${PROD_BASE_URL}/weather/`)
        .then(response => {
          this.weather.temperature = response.data.temperature;
          this.weather.icon = response.data.icon;
          this.weather.condition = response.data.condition;
          this.weather.surge = response.data.surge;
        })
        .catch(error => {
          console.error('Error fetching weather data:', error);
        })
    },

    showPaymentModal(type) {
      this.paymentType = type;
      this.paymentModal = true;
    },
    closePaymentModal() {
      this.paymentModal = false;
      this.paymentType = null;
      this.creditCardNumber = '';
      this.expirationDate = '';
      this.cvv = '';
    },
    addToCart(item) {
      this.cartItems.push(item);
    },
    removeFromCart(index) {
      this.cartItems.splice(index, 1);
    },
    async checkout() {
      try {
        this.isSubmitting = true;
        const user = getCookie("id") || 1;
        const orderData = { status: 0, total: this.calculateTotal, timestamp: new Date().toISOString(), employee: user };
        this.updatePoints();
        const orderResponse = await axios.post(`${PROD_BASE_URL}/order/`, orderData);
        const order_id = orderResponse.data.id;

        for (const item of this.cartItems) {
          const orderMenuItem = { order: order_id, menu: item.id, quantity: 1 };
          await axios.post(`${PROD_BASE_URL}/order_menu/`, orderMenuItem);
        }
        this.isSubmitting = false;

        this.cartItems = [];
        alert(`Thank you for your purchase! Your order number is ${order_id}`);
        window.location.reload()
      } catch (error) {
        alert("Something went wrong");
        console.error('Error submitting order:', error);
      }
      this.isSubmitting = false;
    },
    formatPrice(price) {
      const USDFormatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      });
      return USDFormatter.format(price)
    },

    updatePoints() {
      const userID = getCookie("id") || 1;
      axios.patch(`${PROD_BASE_URL}/user/${userID}/`, { points: parseInt(this.calculateTotal*100) });
    },

     startLiveReload(initalDelay = 2000, proceedDelay = 1000){
      const self = this
      this.reloadTimeout = setTimeout(async function updateMenu (){
         self.fetchMenuItems()
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
    },},

   mounted(){
    this.startLiveReload()
  },
  beforeRouteLeave(to, from, next){
    this.stopLiveReload()
    next()
  }

}
</script>
<style scoped>
body {
  min-height: 100vh;
  margin: 0;
  padding: 0;
  color: black;
}

.tab {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
  text-align: center;
  position: relative;
}

.tab button {
  background-color: inherit;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
}

.tab button.cart-button {
  position: absolute;
  top: 0;
  right: 0;
}

.tab button.image-button {
  position: absolute;
  top: 0;
  left: 0;
}

.tab button:hover {
  background-color: #ddd;
  transition: background-color 0.3s ease;
}

.tab button.active {
  background-color: #ccc;
}

.tab button:focus,
.tab li:focus-within {
  outline: none; /* Remove the default outline */
  background-color: rgba(59, 130, 246, 0.5); /* Change the background color on focus */
}

.menu-container {
  display: flex;
  flex-wrap: wrap;
  text-align: center;
}

.checkout-button {
  display: block;
  margin-top: 20px;
  border: 2px solid #ccc;
  border-radius: 5%;
}

.menu-item {
  margin: 5px;
  padding: 10px;
  border-radius: 5px;
  width: calc(20% - 40px);
  background-color: white;
}

.item-details {
  color: black;
  margin-top: 10px;
}

.price {
  font-weight: bold;
  color: black;
}

.cart {
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  position: absolute;
  top: 50px;
  right: 0;
  z-index: 999;
}

.edit {
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  position: absolute;
  top: 50%;
  right: 50%;
}

.add-button {
  background-color: #ccc;
  border: none;
  border-radius: 5px;
  color: #333;
  padding: 10px;
  cursor: pointer;
}

.add-button:hover {
  background-color: #388e3c;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.cart-item-details {
  display: flex;
  flex-direction: column;
}

.cart-totals {
  margin-top: 20px;
  border-top: 1px solid #ccc;
  padding-top: 10px;
}

.cart-total {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.payment-options {
  margin-top: 20px;
}

.payment-option {
  display: block;
  margin-bottom: 10px;
  padding: 10px 20px;
  background-color: #ccc;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.payment-option:hover {
  background-color: #888;
  transition: background-color 0.3s ease;
}

.payment-modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 30%;
}

.close {
  background-color: #ff6961;
  float: right;
  font-weight: bold;
  border-radius: 4px;
  padding: 0.5rem 1rem;
}

.close:hover,
.close:focus {
  background-color:#e53935;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit {
  background-color: #4caf50;
  color: white;
  transition: background-color 0.3s ease;
}

.credit-card-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.form-group input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-button {
  padding: 0.5rem 1rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #388e3c;
  transition: background-color 0.3s ease;
}

.cart-modal {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  height: 90%;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.modal-content {
  padding: 20px;
  position: relative;
}

.remove-button {
  background-color: #ff6961;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.remove-button:hover {
  background-color: #e53935;
  transition: background-color 0.3s ease;
}

img {
  max-width: 200px;
  max-height: 200px;
  padding-left: 25%;
  object-fit: contain;
}

.hidden {
  display: none;
}

</style>