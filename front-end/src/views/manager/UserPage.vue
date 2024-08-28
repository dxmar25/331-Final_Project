<template>
    <div class="flex flex-wrap mt-14">
        <div class="w-full mb-12 px-4 w-full">
            <UserTable
            :userData="userData"
            @editUser="editUser"
            @saveUser="saveUser"
            @deleteUser="deleteUser"
            class="mb-8"
            />
        </div>
    </div>
  </template>

<script>
import UserTable from "@/components/Cards/UserTable.vue";
import axios from 'axios';
import { OrderStatus, PROD_BASE_URL } from '../../main';

export default {
  components: {
    UserTable,
  },
  data() {
    return {
      userData: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get(`${PROD_BASE_URL}/user`)
        .then(response => {
          this.userData = response.data;
        })
        .catch(error => {
          console.error('Error fetching order history data:', error);
        });
    },
    editUser(user) {
      const index = this.userData.findIndex(u => u.id === user.id);
      if (index !== -1) {
        this.userData[index].editing = true;
      }
    },
    async saveUser(user) {
      const index = this.userData.findIndex(u => u.id === user.id);
      if (index !== -1) {
        try {
          const response = await axios.put(`${PROD_BASE_URL}/user/${user.id}/`, user);
          this.userData[index] = { ...user, editing: false };
        } catch (error) {
          console.error('Error saving user:', error);
          alert('Failed to save user. Please try again.');
        }
      }
    },
    async deleteUser(user) {
      if (confirm(`Are you sure you want to delete ${user.name}?`)) {
        try {
          const response = await axios.delete(`${PROD_BASE_URL}/user/${user.id}`);
          this.userData = this.userData.filter(u => u.id !== user.id);
        } catch (error) {
          console.error('Error deleting user:', error);
        }
      }
    },
  }
};
</script>


