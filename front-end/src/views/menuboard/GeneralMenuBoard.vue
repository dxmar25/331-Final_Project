<template>
  <div class="bg-primary p-8">
    <div class="menu-container grid grid-cols-1 md:grid-cols-2 gap-4">
      <section class="menu-section" v-if="leftSideItems.length > 0">
        <h1 class="category text-5xl text-center">{{ leftSideItems[currentLeftIndex].category }}</h1>
        <p class="category-desc text-xl text-center mb-4">{{ leftSideItems[currentLeftIndex].description }}</p>

        <!-- ios dots for lhs -->
        <div class="flex justify-center space-x-2 mt-2 pb-4">
          <button
            v-for="(item, index) in leftSideItems"
            :key="index"
            :class="['h-3 w-3 rounded-full', index === currentLeftIndex ? 'bg-blue-500' : 'bg-gray-300']"
            aria-label="Set current page"
          ></button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <menu-item
            v-for="item in leftSideItems[currentLeftIndex].items"
            :key="item.id"
            :name="item.firstValue.name"
            :description="item.firstValue.description"
            :entree="item.secondValue"
            :combo="item.firstValue.price"
            :image="item.firstValue.image"
            class="menu-item"
          />
        </div>
      </section>

      <section class="menu-section" v-if="rightSideItems.length > 0">
        <h1 class="category text-5xl text-center">{{ rightSideItems[currentRightIndex].category }}</h1>
        <p class="category-desc text-xl text-center mb-4">{{ rightSideItems[currentRightIndex].description }}</p>
        
        <!-- ios dots for rhs -->
        <div class="flex justify-center space-x-2 mt-2 pb-4">
          <button
            v-for="(item, index) in rightSideItems"
            :key="index"
            :class="['h-3 w-3 rounded-full', index === currentRightIndex ? 'bg-blue-500' : 'bg-gray-300']"
            aria-label="Set current page"
          ></button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <menu-item
            v-for="item in rightSideItems[currentRightIndex].items"
            :key="item.id"
            :name="item.name"
            :description="item.description"
            :entree="item.price"
            :image="item.image"
            class="menu-item"
          />
        </div>
        
      </section>
    </div>
  </div>
</template>

<script>
import MenuItem from '../../components/Cards/MenuItem.vue';
import axios from 'axios';
import { LOCAL_BASE_URL, MenuCategories } from '../../main';

export default {
  components: {
    'menu-item': MenuItem
  },
  data() {
    return {
      burgers: [], //0
      baskets: [], //1
      sandwiches: [], //2
      shakesNsweets: [], //0
      beverages: [], //1
      sides: [], //2
      sauces: [],//3
      delay: 5000,
      // slideIndices: {
      //   L0: "burgers",
      //   L1: "baskets",
      //   L2: "sandwiches",
      //   R0: "shakesNsweets",
      //   R1: "beverages",
      //   R2: "sides",
      //   R3: "sauces",
      // },
      currentLeftIndex: 0,
      currentRightIndex: 0,
      leftSideItems: [],
      rightSideItems: [],
      leftIntervalId: null,
      rightIntervalId: null,

      imageSources: {
        Burgers: '@/assets/burger.png',
        Baskets: '@/assets/basket.png',
        Sandwiches: '@/assets/sandwich.png',
        'Shakes n Sweets': '@/assets/shake.png',
        Beverages: '@/assets/beverage.png',
        Sides: '@/assets/side.png',
        Sauces: '@/assets/sauce.png',
      }

    };
  },
  mounted() {
    this.init();
  },
  beforeDestroy() {
    clearInterval(this.leftIntervalId);
    clearInterval(this.rightIntervalId);
  },
  methods: {
    async init(){
      this.fetchMenuItems();
      this.startRotating()
    },
    startRotating(){
      this.leftIntervalId = setInterval(() => {
        this.fetchBurgers();
        this.fetchBaskets();
        this.fetchSandwiches();
        this.organizeMenuItems();
        this.rotateItems('left')}, this.delay);
      this.rightIntervalId = setInterval(() => {
        this.fetchShakesNsweets();
        this.fetchBeverages();
        this.fetchSides();
        this.fetchSauces();
        this.organizeMenuItems()
        this.rotateItems('right')}, this.delay);
    },
    currentIndex(side) {
      return side === 'left' ? this.currentLeftIndex : this.currentRightIndex;
    },
    rotateItems(side) {
      if (side === 'left') {
        this.currentLeftIndex = (this.currentLeftIndex + 1) % this.leftSideItems.length;
      } else {
        this.currentRightIndex = (this.currentRightIndex + 1) % this.rightSideItems.length;
      }
    },
    itemDetails(item) {
      return item.firstValue ? item.firstValue : item;
    },
    itemPrice(item) {
      if (item.firstValue) {
        return { entree: item.secondValue, combo: item.firstValue.price };
      } else {
        return { entree: item.price, combo: null };
      }
    },
    async fetchBurgers() {
      await axios.get(`${LOCAL_BASE_URL}/menu/?category=0`)
        .then(response => {
          let count = 0;
          let index = 0;
          let elements = response.data.length;
          console.log(response.data)
          this.burgers = []
          while (count < elements - 8 || index < response.data.length) {    
            let display = response.data[index].display;
            if (display == true) {
              let menu_id = response.data[index].id;
              const nextMenuItem = response.data.find(item => item.id === menu_id + 1);
              const secondValue = nextMenuItem ? nextMenuItem.price : null;
              const tuple = {
                firstValue: response.data[index],
                secondValue: secondValue
              };
              this.burgers.push(tuple);
              count += 1;
            }
            index += 1;
          }
        })
        .catch(error => {
          console.error('Error fetching menu items:', error);
        });
    },
    async fetchBaskets() {
      await axios.get(`${LOCAL_BASE_URL}/menu/?category=1`)
        .then(response => {
          let count = 0;
          let index = 0;
          let elements = response.data.length;
          // console.log(response.data.length)
          this.baskets = []
          while (count < elements - 2 || index < elements) {    
            let display = response.data[index].display;
            if (display == true) {
              let menu_id = response.data[index].id;
              const nextMenuItem = response.data.find(item => item.id === menu_id + 1);
              const secondValue = nextMenuItem ? nextMenuItem.price : null;
              const tuple = {
                firstValue: response.data[index],
                secondValue: secondValue
              };
              this.baskets.push(tuple);
              count += 1;
            }
            index += 1;
          }
        })
        .catch(error => {
          console.error('Error fetching menu items:', error);
        });
    },
    async fetchSandwiches() {
      await axios.get(`${LOCAL_BASE_URL}/menu/?category=2`)
        .then(response => {
          let count = 0;
          let index = 0;
          let elements = response.data.length;
          // console.log(response.data.length)
          this.sandwiches = []
          while (count < elements - 4 || index < elements) {   
            let display = response.data[index].display; 
            if (display == true) {
              let menu_id = response.data[index].id;
              const nextMenuItem = response.data.find(item => item.id === menu_id + 1);
              const secondValue = nextMenuItem ? nextMenuItem.price : null;
              const tuple = {
                firstValue: response.data[index],
                secondValue: secondValue
              };
              this.sandwiches.push(tuple);
              count += 1;
            }
            index += 1;
          }
        })
        .catch(error => {
          console.error('Error fetching menu items:', error);
        });
    },
    async fetchShakesNsweets() {
      await axios.get(`${LOCAL_BASE_URL}/menu/?category=3`)
        .then(response => {
          let count = 0;
          let index = 0;
          let elements = response.data.length;
          this.shakesNsweets = []
          while (count < elements || index < elements) {    
            let display = response.data[index].display;
            if (display == true) {
              this.shakesNsweets.push(response.data[index]);
              count += 1;
            }
            index += 1;
          }
        })
        .catch(error => {
          console.error('Error fetching menu items:', error);
        });
    },
    async fetchBeverages() {
      await axios.get(`${LOCAL_BASE_URL}/menu/?category=4`)
        .then(response => {
          let count = 0;
          let index = 0;
          let elements = response.data.length;
          this.beverages = []
          while (count < elements|| index < elements) {    
            let display = response.data[index].display;
            if (display == true) {
              this.beverages.push(response.data[index]);
              count += 1;
            }
            index += 1;
          }
        })
        .catch(error => {
          console.error('Error fetching menu items:', error);
        });
    },
    async fetchSides() {
      await axios.get(`${LOCAL_BASE_URL}/menu/?category=5`)
        .then(response => {
          let count = 0;
          let index = 0;
          let elements = response.data.length;
          this.sides = []
          while (count < elements || index < elements) {    
            let display = response.data[index].display;
            if (display == true) {
              this.sides.push(response.data[index]);
              count += 1;
            }
            index += 1;
          }
        })
        .catch(error => {
          console.error('Error fetching menu items:', error);
        });
    },
    async fetchSauces() {
      await axios.get(`${LOCAL_BASE_URL}/menu/?category=6`)
        .then(response => {
          let count = 0;
          let index = 0;
          let elements = response.data.length;
          this.sauces = []
          while (count < elements || index < elements) {    
            let display = response.data[index].display;
            if (display == true) {
              this.sauces.push(response.data[index]);
              count += 1;
            }
            index += 1;
          }
        })
        .catch(error => {
          console.error('Error fetching menu items:', error);
        });
    },
    async fetchMenuItems() {

      //split for quicker page load
      await axios.all([this.fetchBurgers(), this.fetchBaskets(), this.fetchShakesNsweets(), this.fetchBeverages()]).then(axios.spread((...responses)=>{
        this.organizeMenuItems()
      })).catch(errors => {
        console.error('An error occurred while fetching menu categories:', errors);
      });

      await axios.all([this.fetchSandwiches(), this.fetchSides(), this.fetchSauces()]).then(axios.spread((...responses)=>{
        this.organizeMenuItems()
      })).catch(errors => {
        console.error('An error occurred while fetching menu categories:', errors);
      });

      // axios.all([
      //   this.fetchBurgers(),
      //   this.fetchBaskets(),
      //   this.fetchSandwiches(),
      //   this.fetchShakesNsweets(),
      //   this.fetchBeverages(),
      //   this.fetchSides(),
      //   this.fetchSauces(),
      // ]).then(axios.spread((...responses) => {
      //   this.organizeMenuItems();
      // })).catch(errors => {
      //   console.error('An error occurred while fetching menu categories:', errors);
      // });
    },
    organizeMenuItems() {
      this.leftSideItems = [
        { category: 'Burgers', description: 'Choose a Beef or Chipotle Black Bean Patty. All Combos include a Fountain Drink and Fries.', items: this.burgers },
        { category: 'Baskets', description: 'All Combos Include a Fountain Drink', items: this.baskets },
        { category: 'Sandwiches', description: 'All Combos include a Fountain Drink and Fries.', items: this.sandwiches },
      ];
      this.rightSideItems = [
        { category: 'Shakes n Sweets', description: 'Sweeten up your day!', items: this.shakesNsweets },
        { category: 'Beverages', description: 'Always refreshing!', items: this.beverages },
        { category: 'Sides', description: 'Oh, what to choose?', items: this.sides },
        { category: 'Sauces', description: 'Enjoy our specially selected sauces.', items: this.sauces },
      ];
    },
  }
};
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@900&family=Roboto+Slab&display=swap');

.category {
  font-family: 'Exo 2', sans-serif;
  font-size: 4xl; 
  font-weight: 900; 
  color: #f9c2c2; 
  margin-bottom: 0.25rem;
}

.category-desc {
  font-family: 'Roboto Slab', serif;
  font-size: xl; 
  color: #FFF3E0; 
  opacity: 0.9;
  letter-spacing: 0.05em; 
}


</style>