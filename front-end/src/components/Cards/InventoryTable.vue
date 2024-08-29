<template>
    <div class="inventory-wrapper my-8">
        <div class="my-8">
            <div class="mb-4 inventory-header">
                <h1 class="text-3xl font-bold text-red-600">Inventory</h1>
            </div>

            <div class="relative overflow-x-auto shadow-lg rounded-lg">
                <table class="w-full text-sm text-left text-gray-900">
                    <thead class="text-sm text-red-700 uppercase bg-red-100">
                        <tr>
                            <th scope="col" class="px-6 py-3">Product Name</th>
                            <th scope="col" class="px-6 py-3">Price</th>
                            <th scope="col" class="px-6 py-3">Stock</th>
                            <th scope="col" class="px-6 py-3">Reorder Level</th>
                            <th scope="col" class="px-6 py-3">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in paginatedData" :key="item.id"
                            :class="{ 'bg-red-200': item.stock < item.reorder_level }">
                            <th scope="row" class="px-6 py-4 font-medium text-gray-900">
                                <template v-if="item.editing">
                                    <input v-model="item.name" class="px-2 py-1" />
                                </template>
                                <template v-else>
                                    {{ item.name }}
                                </template>
                            </th>
                            <td class="px-6 py-4">
                                <template v-if="item.editing">
                                    <input v-model="item.price" type="number" class="px-2 py-1" />
                                </template>
                                <template v-else>
                                    ${{ item.price.toFixed(2) }}
                                </template>
                            </td>
                            <td class="px-6 py-4">
                                <template v-if="item.editing">
                                    <input v-model="item.stock" type="number" class="px-2 py-1" />
                                </template>
                                <template v-else>
                                    {{ item.stock }}
                                </template>
                            </td>
                            <td class="px-6 py-4">
                                <template v-if="item.editing">
                                    <input v-model="item.reorder_level" type="number" class="px-2 py-1" />
                                </template>
                                <template v-else>
                                    {{ item.reorder_level }}
                                </template>
                            </td>
                            <td class="px-6 py-4 text-center">
                                <template v-if="item.editing">
                                    <img src="@/assets/save.png" alt="Save" @click="saveItem(item)"
                                        class="action-icon cursor-pointer" />
                                </template>
                                <template v-else>
                                    <div class="flex justify-center items-center">
                                        <img src="@/assets/edit2.png" alt="Modify" @click="editItem(item)"
                                            class="action-icon cursor-pointer" />
                                        <img src="@/assets/delete3.png" alt="Delete" @click="deleteItem(item)"
                                            class="action-icon cursor-pointer" />
                                    </div>
                                </template>
                            </td>

                        </tr>
                    </tbody>
                </table>
                <div class="flex justify-between items-center p-4 text-md text-red-700 uppercase bg-gray-50">
                    <button @click="currentPage > 1 && currentPage--" :disabled="currentPage <= 1">
                        Previous
                    </button>
                    <span>Page {{ currentPage }} of {{ totalPages }}</span>
                    <button @click="currentPage < totalPages && currentPage++" :disabled="currentPage >= totalPages">
                        Next
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import InventoryModal from "@/components/Modal/Modal.vue";
import { OrderStatus, PROD_BASE_URL } from '../../main';

export default {
    props: {
        inventoryData: {
            type: Array,
            required: true,
        },
    },
    data() {
        return {
            currentPage: 1,
            perPage: 10,
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.inventoryData.length / this.perPage);
        },
        paginatedData() {
            const start = (this.currentPage - 1) * this.perPage;
            const end = start + this.perPage;
            return this.inventoryData.slice(start, end);
        }
    },
    methods: {
        editItem(item) {
            this.$emit('editItem', item);
        },
        saveItem(item) {
            this.$emit('saveItem', item);
        },
        deleteItem(item) {
            this.$emit('deleteItem', item);
        },
        fetchInventory() {
            this.$emit('fetchInventory');
        }
    }
};
</script>

<style>
.inventory-wrapper .inventory-header h1 {
    margin-bottom: 1rem;
    padding-bottom: .5rem;
    border-bottom: 2px solid #feb2b2;
    display: inline-block;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.inventory-wrapper .inventory-table {
    border-collapse: separate;
    border-spacing: 0;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.inventory-wrapper th,
.inventory-wrapper td {
    border: 1px solid #e2e8f0;
}

.inventory-wrapper thead,
.inventory-wrapper .flex.justify-between {
    background-image: linear-gradient(to right, #feb2b2, #ee7676);
}

.inventory-wrapper tbody tr.bg-red-200,
.inventory-wrapper tbody tr.bg-red-200:nth-child(odd),
.inventory-wrapper tbody tr.bg-red-200:nth-child(even) {
    background-color: #f5ff9b !important;
}

.inventory-wrapper tbody tr:not(.bg-red-200):nth-child(odd) {
    background-color: #e3e5e7;
}

.inventory-wrapper tbody tr:not(.bg-red-200):nth-child(even) {
    background-color: #edf2f7;
}

.inventory-wrapper tbody tr:not(.bg-red-200):hover,
.inventory-wrapper tbody tr.bg-red-200:hover {
    background-color: #a2b9de !important;
}

.inventory-wrapper thead th {
    font-weight: 600;
    font-family: Arial, sans-serif;
}

.inventory-wrapper .flex.justify-between {
    border-top: 3px solid #fc8181;
    text-align: center;
}

.action-icon {
    width: 30px;
    height: auto;
    margin-left: 8px;
}

.text-gray-900 {
    color: #1a202c;
}
</style>
