<template>
    <div class="flex flex-wrap mt-14">
      <div class="w-full mb-12 px-4 w-full">
            <InventoryTable 
            :inventoryData="inventoryData" 
            @editItem="editItem" 
            @saveItem="saveItem"
            @deleteItem="deleteItem" 
            @fetchInventory="fetchInventory" 
            class="mb-8"
            />
        </div>
      </div>
</template>

<script>
import InventoryTable from "@/components/Cards/InventoryTable.vue";
import axios from 'axios';
import { OrderStatus, PROD_BASE_URL } from '../../main';

export default {
  components: {
    InventoryTable,
  },
  data() {
    return {
      inventoryData: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get(`${PROD_BASE_URL}/inventory`)
        .then(response => {
          this.inventoryData = response.data;
        })
        .catch(error => {
          console.error('Error fetching inventory data:', error);
        });
    },
    editItem(item) {
      const index = this.inventoryData.findIndex(i => i.id === item.id);
      if (index !== -1) {
        this.inventoryData[index].editing = true;
      }
    },
    async saveItem(item) {
      const index = this.inventoryData.findIndex(i => i.id === item.id);
      if (index !== -1) {
        try {
          const response = await axios.put(`${PROD_BASE_URL}/inventory/${item.id}/`, item);
          console.log("Save response:", response.data);
          this.inventoryData[index] = { ...item, editing: false };
        } catch (error) {
          console.error('Error saving inventory item:', error);
          alert('Failed to save item. Please try again.');
        }
      }
    },
    async deleteItem(item) {
      if (confirm(`Are you sure you want to delete ${item.name}?`)) {
        try {
          const response = await axios.delete(`${PROD_BASE_URL}/inventory/${item.id}`);
          console.log("Delete response:", response.data);
          this.inventoryData = this.inventoryData.filter(i => i.id !== item.id);
        } catch (error) {
          console.error('Error deleting inventory item:', error);
        }
      }
    },
    fetchInventory() {
      axios.get(`${PROD_BASE_URL}/inventory`)
        .then(response => {
          this.inventoryData = response.data;
        })
        .catch(error => {
          console.error('Failed to fetch inventory:', error);
        });
    },
  }
};
</script>