<template>
  <div class="menu-item flex flex-col items-center text-center p-4 bg-black rounded-lg shadow-md">
    <img :src="image" :alt="imageText" class="w-32 h-32 mx-auto">
    <h2 class="item-name text-2xl font-semibold mt-2">{{ name }}</h2>
    <p class="description text-md mt-1">{{ description }}</p>
    <p class="price text-lg font-bold mt-2" v-if="combo && entree">Combo: ${{ combo }} <br> Entree: ${{ entree }}</p>
    <p class="price text-lg font-bold mt-2" v-else-if="entree">Price: ${{ entree }}</p>
    <p class="price text-lg font-bold mt-2" v-else-if="combo">Price: ${{ combo }}</p>
    <p class="price text-lg font-bold mt-2" v-else>Price unavailable</p>
  </div>
</template>


<script>
import filler from '@/assets/burger.png'
import { PROD_BASE_URL } from '../../main';
import axios from 'axios';


export default {
  props: {
    name: String,
    description: String,
    entree: Number,
    combo: Number,
    image: String,
  },
  data() {
    return {
      imageText: 'Menu Item Image',
    }
  },
  mounted() {
    // console.log('Props in MenuItem:', this.name, this.combo, this.entree, this.image);
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600&family=Lato&display=swap');

.item-name {
  font-family: 'Oswald', sans-serif;
  font-size: 2xl; 
  font-weight: 600; 
  color: #FFFFFF; 
  text-transform: uppercase; 
}

.description {
  font-family: 'Lato', sans-serif;
  font-size: md; 
  color: #BBBBBB; 
}

.price {
  font-family: 'Lato', sans-serif;
  font-size: lg; 
  font-weight: bold;
  color: #4CAF50; 
}

</style>
