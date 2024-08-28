<template>
  <form @submit.prevent="submitForm" class="max-w-xl mx-auto p-8 shadow-lg rounded-lg bg-white">
    <h2 class="text-2xl font-semibold text-gray-800 mb-6">Create Menu Item</h2>
    
    <div class="mb-4">
      <label for="itemName" class="block text-gray-700 text-sm font-bold mb-2">Name:</label>
      <input type="text" id="itemName" v-model.trim="form.name" required
             placeholder="Burger"
             class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
    </div>

    <div class="mb-4">
      <label for="itemPrice" class="block text-gray-700 text-sm font-bold mb-2">Price ($):</label>
      <input type="number" id="itemPrice" v-model.number="form.price" required min="0"
             placeholder="13.0"
             class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
    </div>

    <div class="mb-4">
      <label for="itemCategory" class="block text-gray-700 text-sm font-bold mb-2">Category:</label>
      <select id="itemCategory" v-model.number="form.category" required
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        <option disabled value="">Select a category</option>
        <option value="0">Burgers</option>
        <option value="1">Baskets</option>
        <option value="2">Sandwiches</option>
        <option value="3">Shakes & Sweets</option>
        <option value="4">Beverages</option>
        <option value="5">Sides</option>
        <option value="6">Sauces</option>
      </select>
    </div>

    <div class="mb-4">
      <label for="itemDescription" class="block text-gray-700 text-sm font-bold mb-2">Description:</label>
      <textarea id="itemDescription" v-model="form.description"
                placeholder="Juicy burger"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"></textarea>
    </div>

    <div class="mb-4 flex gap-4">
      <div class="w-1/2">
        <label for="itemSeasonStart" class="block text-gray-700 text-sm font-bold mb-2">Season Start:</label>
        <input type="date" id="itemSeasonStart" v-model="form.season_start" required
               class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
      </div>
      <div class="w-1/2">
        <label for="itemSeasonEnd" class="block text-gray-700 text-sm font-bold mb-2">Season End:</label>
        <input type="date" id="itemSeasonEnd" v-model="form.season_end" required
               class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
      </div>
    </div>

    <div class="mb-4">
      <label for="itemImageURL" class="block text-gray-700 text-sm font-bold mb-2">Image URL:</label>
      <input type="url" id="itemImageURL" v-model="form.image_url" required
             placeholder="http://example.com/burger.png"
             class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
    </div>

    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2">Display:</label>
      <input type="checkbox" id="itemDisplay" v-model="form.display"
             class="leading-tight">
      <span class="text-sm">Yes</span>
    </div>

    <button type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
      Create Menu Item
    </button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        price: null,
        category: null,
        description: '',
        season_start: '',
        season_end: '',
        display: true,  
        image_url: ''
      }
    };
  },
  methods: {
    submitForm() {
      this.$emit('create-menu-item', this.form);
    }
  }
};
</script>
