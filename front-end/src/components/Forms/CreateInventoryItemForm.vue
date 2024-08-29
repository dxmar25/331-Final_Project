<template>
    <form @submit.prevent="submitForm" class="max-w-xl mx-auto p-8 shadow-lg rounded-lg bg-white">
      <h2 class="text-2xl font-semibold text-gray-800 mb-6">Create Inventory Item</h2>
  
      <div class="mb-4">
        <label for="itemName" class="block text-gray-700 text-sm font-bold mb-2">Name:</label>
        <input type="text" id="itemName" v-model.trim="form.name" required
               placeholder="American Cheese"
               class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
      </div>
  
      <div class="mb-4">
        <label for="itemPrice" class="block text-gray-700 text-sm font-bold mb-2">Price ($):</label>
        <input type="number" id="itemPrice" v-model.number="form.price" required min="0" step="0.01"
               placeholder="0.25"
               class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
      </div>
  
      <div class="mb-4">
        <label for="itemStock" class="block text-gray-700 text-sm font-bold mb-2">Stock:</label>
        <input type="number" id="itemStock" v-model.number="form.stock" required min="0"
               placeholder="500"
               class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
      </div>
  
      <div class="mb-6">
        <label for="itemReorderLevel" class="block text-gray-700 text-sm font-bold mb-2">Reorder Level:</label>
        <input type="number" id="itemReorderLevel" v-model.number="form.reorder_level" required min="0"
               placeholder="100"
               class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
      </div>
  
      <button type="submit"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
        Create Inventory Item
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
          stock: null,
          reorder_level: null
        }
      };
    },
    methods: {
      submitForm() {
        this.$emit('create-item', this.form);
      },
    }
  };
  </script>
  