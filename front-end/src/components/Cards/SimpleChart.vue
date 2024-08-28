<script>
import TableDropdown from "@/components/Dropdowns/TableDropdown.vue";

export default {
  components: {
    TableDropdown,
  },
  props: {
    color: {
      default: "light",
      validator: function (value) {
        return ["light", "dark"].indexOf(value) !== -1;
      },
    },
  },
};
</script>


<template>
<div class="relative overflow-x-auto">
    <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" class="px-6 py-3">
                    Inventory Item Name
                </th>
                
                <th scope="col" class="px-6 py-3">
                    Quantity Used
                </th>
            </tr>
        </thead>
        <tbody> <!-- start auto populating here -->
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    Lettice <!-- name -->
                </th>
                <td class="px-6 py-4">
                    4 <!-- quantity -->
                </td>
            </tr>
        </tbody>
    </table>
</div>

</template>