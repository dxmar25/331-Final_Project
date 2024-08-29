<template>
    <div class="container">
        <div class="datepicker-container">
        <Datepicker class="datepicker" v-model="startDate" model-type="yyyy-MM-dd" placeholder="Select Start Date" :enable-time-picker="false" :disabled="isRestockReportSelected"/>
        <Datepicker class="datepicker" v-model="endDate" model-type="yyyy-MM-dd" placeholder="Select End Date" :enable-time-picker="false" :disabled="isExcessReportSelected || isRestockReportSelected"/>
        </div>
        <p></p>
        <div class="date-info">
            <p v-if="startDate && endDate">Start date: {{ startDate }}</p>
            <p v-if="startDate && endDate">End date: {{ endDate }}</p>
        </div>
        <div class="dropdown">
            <button class="dropdown-toggle" @click="toggleDropdown">{{ selectedOption.name || 'Select A Query' }}</button>
            <div class="dropdown-menu" v-if="isOpen">
                <a class="dropdown-item" v-for="option in options" :key="option.name" @click="selectOption(option)">{{ option.name }}</a>
            </div>
        </div>  
        <p class="description"> {{ selectedOption.description }}</p>
        <button class="run-button" v-if="isSelected" @click="selectedOption.fetch">Run</button>
        <div v-if="selectedOption.type === '1'" class="relative overflow-x-auto">
            <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th scope="col" class="px-6 py-3">
                            {{ selectedOption.col_1 }}
                        </th>
                        <th scope="col" class="px-6 py-3">
                            {{ selectedOption.col_2 }}
                        </th>
                        <th scope="col" class="px-6 py-3">
                            {{ selectedOption.col_3 }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in selectedArray" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            {{ product.name }}
                        </th>
                        <td class="px-6 py-4">
                            {{ product.count }}
                        </td>
                        <td class="px-6 py-4">
                            {{ product.option }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="selectedOption.type === '2'" class="relative overflow-x-auto">
            <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th scope="col" class="px-6 py-3">
                            {{ selectedOption.col_1  }}
                        </th>
                    
                        <th scope="col" class="px-6 py-3">
                            {{ selectedOption.col_2  }}
                        </th>
                    </tr>
                </thead>
                <tbody> <!-- start auto populating here -->
                    <tr v-for="product in selectedArray" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            {{ product.name }} <!-- name -->
                        </th>
                        <td class="px-6 py-4">
                            {{ product.count }} <!-- quantity -->
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="selectedOption.type === '3'" class="relative overflow-x-auto">
            <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th scope="col" class="px-6 py-3">
                            {{ selectedOption.col_1 }}
                        </th>
                        <th scope="col" class="px-6 py-3">
                            {{ selectedOption.col_2 }}
                        </th>
                        <th scope="col" class="px-6 py-3">
                            {{ selectedOption.col_3 }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in selectedArray" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            {{ product.element1 }}
                        </th>
                        <td class="px-6 py-4">
                            {{ product.element2 }}
                        </td>
                        <td class="px-6 py-4">
                            {{ product.element3 }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
    </div>
</template>

<script>
  import { ref } from 'vue';
  import Datepicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';
  import TableDropdown from "@/components/Dropdowns/TableDropdown.vue";
  import axios from 'axios';
  import { MenuCategories, PROD_BASE_URL } from '../../main';
  
  export default {
    components: {
        Datepicker,
        TableDropdown
    },
    props: {
        color: {
            default: "light",
            validator: function (value) {
                return ["light", "dark"].indexOf(value) !== -1;
            },
        },
    },
    data() {
        return {
            productUsage: [],
            salesReport: [],
            excessItems: [],
            restockReport: [],
            sellsTogethor: [],
            startDate: ref(""),
            endDate: ref(""),
            isOpen: false,
            isSelected: false,
            selectedOption: { name: 'default', type: '1', col_1: 'Place Holder', col_2: 'Place Holder', col_3: 'Place Holder', fetch: null },
            options: [
                { name: 'Product Usage Table', type: '2', col_1: 'Item Name', col_2: 'Quantity Used', fetch: this.fetchProductUsage, description: 'Given a time window it displays the number of each inventory item used during that time period.' }, // will use .name and .count to get the elements out of array 
                { name: 'Sales Report', type: '3', col_1: 'Item Name', col_2: 'Quantity Sold', col_3: 'Revenue', fetch: this.fetchSalesReport, description: 'Given a time window it displays the number and revenue of each menu item sold during that time period.' }, // will use .element1 , .element2 , .element3 
                { name: 'Excess Report', type: '3', col_1: 'Item Name', col_2: 'Quantity Used', col_3: 'Current Stock', fetch: this.fetchExcessItems, description: 'Given a timestamp, it displays the list of inventory items that sold less than 10% of their quantity between the timestamp and the current time.'},
                { name: 'Restock Report', type: '3', col_1: 'Item Name', col_2: 'Current Amount', col_3: 'Restock Level', fetch: this.fetchRestockReport, description: 'Displays a list of inventory items whose current stock is less than the items reorder level'},
                { name: 'Common Pairings', type: '3', col_1: 'Item Pair 1', col_2: 'Item Pair 2', col_3: 'Pairings', fetch: this.fetchSellsTogethor, description: 'Given a time window, it displays a list of pairs of menu items that sell together, sorted by most frequent.'},
            ],
            defaultData: [
                { name: 'Name 1', count: '' , option: ''},
                { name: 'Name 2', count: '' , option: ''},
                { name: 'Name 3', count: '' , option: ''},
                { name: 'Name 4', count: '' , option: ''},
                { name: 'Name 5', count: '' , option: ''}
            ],
        }   
    },
    computed: {
        selectedArray() {
            switch (this.selectedOption.name) {
                case 'Product Usage Table':
                    return this.productUsage;
                case 'Sales Report':
                    return this.salesReport;
                case 'Excess Report':
                    return this.excessItems;
                case 'Restock Report':
                    return this.restockReport;
                case 'Common Pairings':
                    return this.sellsTogethor;
                case 'default':
                    return this.defaultData ;
                default:
                    return [];
            }
        },
        isExcessReportSelected() {
            return this.selectedOption && this.selectedOption.name === 'Excess Report';
        },
        isRestockReportSelected() {
            return this.selectedOption && this.selectedOption.name === 'Restock Report';
        },
    },  
    methods: {
        fetchProductUsage() {
            axios.get(`${PROD_BASE_URL}/product_usage_chart_data/`, {
                params: {
                    // "2022-03-29 00:00:00"
                    // "2024-03-28 23:59:59"
                startDate: this.startDate.concat(" 00:00:00"),
                endDate: this.endDate.concat(" 23:59:59")
                }
            })
            .then(response => {
                this.productUsage = response.data;
            })
            .catch(error => {
                console.error('Error:', error);
            });
            this.isSelected = false;
        },
        fetchSalesReport() {
            axios.get(`${PROD_BASE_URL}/sales_report/`, {
                params: {
                    // "2022-03-29 00:00:00"
                    // "2024-03-28 23:59:59"
                startDate: this.startDate.concat(" 00:00:00"),
                endDate: this.endDate.concat(" 23:59:59")
                }
            })
            .then(response => {
                this.salesReport = response.data;
            })
            .catch(error => {
                console.error('Error:', error);
            });
            this.isSelected = false;
        },
        fetchExcessItems() {
            axios.get(`${PROD_BASE_URL}/excess_report/`, {
                params: {
                    // "2024-03-28 23:59:59"
                endDate: this.endDate.concat(" 23:59:59")
                }
            })
            .then(response => {
                this.excessItems = response.data;
            })
            .catch(error => {
                console.error('Error:', error);
            });
            this.isSelected = false;
        },
        fetchRestockReport() {
            axios.get(`${PROD_BASE_URL}/restock_report/`)
            .then(response => {
                this.restockReport = response.data;
            })
            .catch(error => {
                console.error('Error:', error);
            });
            this.isSelected = false;
        },
        fetchSellsTogethor() {
            axios.get(`${PROD_BASE_URL}/sells_together/`, {
                params: {
                    // "2022-03-29 00:00:00"
                    // "2024-03-28 23:59:59"
                startDate: this.startDate.concat(" 00:00:00"),
                endDate: this.endDate.concat(" 23:59:59")
                }
            })
            .then(response => {
                this.sellsTogethor = response.data;
            })
            .catch(error => {
                console.error('Error:', error);
            });
            this.isSelected = false;
        },
        toggleDropdown() {
            this.isOpen = !this.isOpen;
        },
        selectOption(option) {
            this.selectedOption = option;
            this.isOpen = false;
            this.isSelected = true;
        },
    }
  }
</script>

<style>
body {
    color: black;
    background-color: #580726; /* This dones not work for some reason */
}

.container {
  max-width: 90%;
  margin: 0 auto;
  padding: 20px;
}

.datepicker-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.datepicker {
  margin: 0 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.date-info {
  text-align: center;
  margin-bottom: 20px;
}

.dropdown {
  position: relative;
  display: inline-block;
  margin-bottom: 20px;
}

.dropdown-toggle {
  background-color: #6d6e6d;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

.dropdown-menu {
  position: absolute;
  background-color: #f9f9f9;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  min-width: 160px;
}

.text-gray-900{
    color: white;
}

@media (prefers-color-scheme: dark) {
    .dark\:text-gray-400 {
        --tw-text-opacity: 1;
        color: white;
    }
}

.disabled-datepicker {
  background-color: #d1d5db; 
  color: #6b7280;
  cursor: not-allowed;
}

.dropdown-item {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-item:hover {
  background-color: #f1f1f1;
}

.description {
  margin-bottom: 20px;
  font-size: 175%;
  color: #000000;
}

.run-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  margin-bottom: 20px;
}

</style>

