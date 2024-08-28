<template>
    <div class="flex flex-wrap mt-14">
      <div class="w-full mb-12 px-4 w-full">
            <MenuTable
            :menuData="menuData"
            @editMenuItem="editMenuItem"
            @saveMenuItem="saveMenuItem"
            @deleteMenuItem="deleteMenuItem"
            class="mb-8"
            />
        </div>
    </div>
</template>

<script>
import MenuTable from "@/components/Cards/MenuTable.vue";
import axios from 'axios';
import { OrderStatus, PROD_BASE_URL } from '../../main';

export default {
  components: {
    MenuTable,
  },
  data() {
    return {
      menuData: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get(`${PROD_BASE_URL}/menu`)
        .then(response => {
          this.menuData = response.data;
        })
        .catch(error => {
          console.error('Error fetching menu data:', error);
        });
    },

    editMenuItem(item) {
      const index = this.menuData.findIndex(i => i.id === item.id);
      if (index !== -1) {
        this.menuData[index].editing = true;
      }
    },
    async saveMenuItem(item) {
      const index = this.menuData.findIndex(i => i.id === item.id);
      if (index !== -1) {
        try {
          const response = await axios.put(`${PROD_BASE_URL}/menu/${item.id}/`, item);
          console.log("Save response:", response.data);
          this.menuData[index] = { ...item, editing: false };
        } catch (error) {
          console.error('Error saving menu item:', error);
          alert('Failed to save menu item. Please try again.');
        }
      }
    },
    async deleteMenuItem(item) {
      if (confirm(`Are you sure you want to delete ${item.name}?`)) {
        try {
          const response = await axios.delete(`${PROD_BASE_URL}/menu/${item.id}`);
          console.log("Delete response:", response.data);
          this.menuData = this.menuData.filter(i => i.id !== item.id);
        } catch (error) {
          console.error('Error deleting menu item:', error);
        }
      }
    },
  }
};
</script>


