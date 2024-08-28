<template>
    <form @submit.prevent="submitForm" class="max-w-xl mx-auto p-8 shadow-lg rounded-lg bg-white">
      <h2 class="text-2xl font-semibold text-gray-800 mb-6">Create User</h2>
  
      <div class="mb-4">
        <label for="userName" class="block text-gray-700 text-sm font-bold mb-2">Name:</label>
        <input type="text" id="userName" v-model.trim="form.name" required
               placeholder="Enter name"
               class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
      </div>
  
      <div class="mb-4">
        <label for="userEmail" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
        <input type="email" id="userEmail" v-model.trim="form.email" required
               placeholder="example@gmail.com"
               class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
      </div>
  
      <div class="mb-4">
        <label for="userType" class="block text-gray-700 text-sm font-bold mb-2">User Type:</label>
        <select id="userType" v-model.number="form.user_type" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
          <option disabled value="">Please select one</option>
          <option value="0">Customer</option>
          <option value="1">Kitchen</option>
          <option value="2">Cashier</option>
          <option value="3">Manager</option>
          <option value="4">Admin</option>
        </select>
      </div>
  
      <div class="mb-4 flex gap-4">
        <div class="w-1/2">
          <label for="userShiftStart" class="block text-gray-700 text-sm font-bold mb-2">Shift Start:</label>
          <input type="datetime-local" id="userShiftStart" v-model="form.shift_start"
                 class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        </div>
        <div class="w-1/2">
          <label for="userShiftEnd" class="block text-gray-700 text-sm font-bold mb-2">Shift End:</label>
          <input type="datetime-local" id="userShiftEnd" v-model="form.shift_end"
                 class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        </div>
      </div>
  
      <button type="submit"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
        Create User
      </button>
    </form>
  </template>
  
  <script>
  export default {
    data() {
      return {
        form: {
          name: '',
          email: '',
          user_type: '',
          shift_start: null,
          shift_end: null
        }
      };
    },
    methods: {
      submitForm() {
        this.$emit('create-user', this.form);
      }
    }
  };
  </script>
  