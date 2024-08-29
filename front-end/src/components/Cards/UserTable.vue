<template>
    <div class="inventory-wrapper my-8">
        <div class="my-8">
            <div class="mb-4 inventory-header">
                <h1 class="text-3xl font-bold text-red-600">Users</h1>
            </div>
            <div class="relative overflow-x-auto shadow-md rounded-lg">
                <table class="w-full text-sm text-left text-gray-900">
                    <thead class="text-xs text-red-700 uppercase bg-gray-50">
                        <tr>
                            <th scope="col" class="px-6 py-3">Name</th>
                            <th scope="col" class="px-6 py-3">Email</th>
                            <th scope="col" class="px-6 py-3">User Type</th>
                            <th scope="col" class="px-6 py-3">Shift Start</th>
                            <th scope="col" class="px-6 py-3">Shift End</th>
                            <th scope="col" class="px-6 py-3">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in paginatedData" :key="item.id" class="bg-white border-b">
                            <td class="px-6 py-4" v-if="item.editing">
                                <input v-model="item.name" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4 font-medium text-gray-900" v-else>{{ item.name }}</td>
                            <td class="px-6 py-4" v-if="item.editing">
                                <input v-model="item.email" type="email" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4" v-else>{{ item.email }}</td>
                            <td class="px-6 py-4" v-if="item.editing">
                                <select v-model="item.user_type" class="px-2 py-1">
                                    <option value="0">Customer</option>
                                    <option value="1">Kitchen</option>
                                    <option value="2">Cashier</option>
                                    <option value="3">Manager</option>
                                    <option value="4">Admin</option>
                                </select>
                            </td>
                            <td class="px-6 py-4" v-else>{{ getUserType(item.user_type) }}</td>
                            <td class="px-6 py-4" v-if="item.editing">
                                <input v-model="item.shift_start" type="time" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4" v-else>{{ item.shift_start }}</td>
                            <td class="px-6 py-4" v-if="item.editing">
                                <input v-model="item.shift_end" type="time" class="px-2 py-1" />
                            </td>
                            <td class="px-6 py-4" v-else>{{ item.shift_end }}</td>
                            <td class="px-6 py-4 text-right">
                                <div class="flex justify-center items-center">
                                    <template v-if="item.editing">
                                        <img src="@/assets/save.png" alt="Save" @click="saveUser(item)"
                                            class="action-icon cursor-pointer" />
                                    </template>
                                    <template v-else>
                                        <img src="@/assets/edit2.png" alt="Modify" @click="editUser(item)"
                                            class="action-icon cursor-pointer" />
                                        <img src="@/assets/delete3.png" alt="Delete" @click="deleteUser(item)"
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
        userData: {
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
            return Math.ceil(this.userData.length / this.perPage);
        },
        paginatedData() {
            const start = (this.currentPage - 1) * this.perPage;
            const end = start + this.perPage;
            return this.userData.slice(start, end);
        }
    },
    methods: {
        editUser(user) {
            this.$emit('editUser', user);
        },
        saveUser(user) {
            this.$emit('saveUser', user);
        },
        deleteUser(user) {
            this.$emit('deleteUser', user);
        },
        fetchUsers() {
            this.$emit('fetchUsers');
        },
        getUserType(type) {
            switch (type) {
                case 0: return 'Customer';
                case 1: return 'Kitchen';
                case 2: return 'Cashier';
                case 3: return 'Manager';
                case 4: return 'Admin';
                default: return 'Unknown';
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