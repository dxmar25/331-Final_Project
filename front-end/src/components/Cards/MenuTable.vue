<template>
    <div class="inventory-wrapper my-8">
        <div class="my-8">
            <div class="mb-4 inventory-header">
                <h1 class="text-3xl font-bold text-red-600">Menu</h1>
            </div>

            <div class="relative overflow-x-auto shadow-lg rounded-lg">
                <table class="w-full text-sm text-left text-gray-900">
                    <thead class="text-sm text-red-700 uppercase bg-red-100">
                        <tr>
                            <th scope="col" class="px-6 py-3">Name</th>
                            <th scope="col" class="px-6 py-3">Price</th>
                            <th scope="col" class="px-6 py-3">Category</th>
                            <th scope="col" class="px-6 py-3">Description</th>
                            <th scope="col" class="px-6 py-3">Season</th>
                            <th scope="col" class="px-6 py-3">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in paginatedData" :key="item.id" class="bg-white border-b">
                            <!-- name-->
                            <td class="px-6 py-4" v-if="item.editing">
                                <input v-model="item.name" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4 font-medium text-gray-900" v-else>{{ item.name }}</td>

                            <!-- price-->
                            <td class="px-6 py-4" v-if="item.editing">
                                <input v-model="item.price" type="number" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4" v-else>${{ item.price.toFixed(2) }}</td>

                            <!-- category-->
                            <td class="px-6 py-4" v-if="item.editing">
                                <input v-model="item.category" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4" v-else>{{ item.category }}</td>

                            <!-- description-->
                            <td class="px-6 py-4" v-if="item.editing">
                                <textarea v-model="item.description" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4" v-else>{{ item.description }}</td>

                            <!-- season-->
                            <td class="px-6 py-4" v-if="item.editing">
                                <input v-model="item.season_start" type="date" class="px-2 py-1" /> -
                                <input v-model="item.season_end" type="date" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4" v-else>{{ formatDate(item.season_start) }} - {{
                                formatDate(item.season_end) }}</td>

                            <!-- actions-->
                            <td class="px-6 py-4 text-right">
                                <div class="flex justify-center items-center">
                                    <template v-if="item.editing">
                                        <img src="@/assets/save.png" alt="Save" @click="saveItem(item)"
                                            class="action-icon cursor-pointer" />
                                    </template>
                                    <template v-else>
                                        <img src="@/assets/edit2.png" alt="Modify" @click="editItem(item)"
                                            class="action-icon cursor-pointer" />
                                        <img src="@/assets/delete3.png" alt="Delete" @click="deleteItem(item)"
                                            class="action-icon cursor-pointer" />
                                    </template>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="flex justify-between items-center p-4 text-md text-red-700 uppercase bg-gray-50">
                    <button @click="currentPage > 1 && currentPage--" :disabled="currentPage <= 1">Previous</button>
                    <span>Page {{ currentPage }} of {{ totalPages }}</span>
                    <button @click="currentPage < totalPages && currentPage++"
                        :disabled="currentPage >= totalPages">Next</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { PROD_BASE_URL } from '../../main';

export default {
    props: {
        menuData: {
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
            return Math.ceil(this.menuData.length / this.perPage);
        },
        paginatedData() {
            const start = (this.currentPage - 1) * this.perPage;
            const end = start + this.perPage;
            return this.menuData.slice(start, end);
        }
    },
    methods: {
        editItem(item) {
            this.$emit('editMenuItem', item);
        },
        saveItem(item) {
            this.$emit('saveMenuItem', item);
        },
        deleteItem(item) {
            this.$emit('deleteMenuItem', item);
        },
        fetchMenu() {
            this.$emit('fetchMenu');
        },
        formatDate(value) {
            if (value) {
                return new Date(value).toLocaleDateString();
            }
        }
    },
};
</script>

<style>
.action-icon {
    width: 30px;
    height: auto;
    margin-left: 8px;
}
</style>
