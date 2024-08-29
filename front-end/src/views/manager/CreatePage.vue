<template>
    <div class="create-page flex flex-wrap justify-around">
      <create-inventory-item-form @create-item="createInventoryItem"></create-inventory-item-form>
      <create-menu-item-form @create-menu-item="createMenuItem"></create-menu-item-form>
      <create-user-form @create-user="createUser"></create-user-form>
    </div>
  </template>

<script>
import CreateInventoryItemForm from '@components/Forms/CreateInventoryItemForm.vue';
import CreateMenuItemForm from '@components/Forms/CreateMenuItemForm.vue';
import CreateUserForm from '@components/Forms/CreateUserForm.vue';


import axios from 'axios';
import { OrderStatus, PROD_BASE_URL } from '../../main';

export default {
    components: {
        CreateInventoryItemForm,
        CreateMenuItemForm,
        CreateUserForm,
    },
    methods: {
        createInventoryItem(itemData) {
            axios.post(`${PROD_BASE_URL}/inventory/`, itemData)
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.error(error);
                });
        },
        createMenuItem(itemData) {
            axios.post(`${PROD_BASE_URL}/menu/`, itemData)
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.error(error);
                });
        },
        createUser(userData) {
            axios.post(`${PROD_BASE_URL}/user/`, userData)
                .then(response => {
                    console.log('User created:', response.data);
                })
                .catch(error => {
                    console.error('Error creating user:', error);
                });
        }
    }
};
</script>

<style scoped>
.create-page {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.create-page > * {
  flex: 1 1 300px;
  margin: 10px;
}

@media (max-width: 768px) {
  .create-page {
    flex-direction: column;
    align-items: center;
  }
  .create-page > * {
    flex: 1 1 100%; 
  }
}
</style>
