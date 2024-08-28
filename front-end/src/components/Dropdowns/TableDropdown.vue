<template>
  <div>
    <a class="text-gray-300 py-1 px-3" href="#pablo" ref="btnDropdownRef" v-on:click="toggleDropdown($event)">
     <i class="fas fa-ellipsis-v"></i>
    </a>

    <div
      ref="popoverDropdownRef"
      class="bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48"
      v-bind:class="{
        hidden: !dropdownPopoverShow,
        block: dropdownPopoverShow,
      }"
    >
      <a
        href="javascript:void(0);"
        class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
      >
        Modify
      </a>
      <a
        href="javascript:void(0);"
        class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
      >
        Delete
      </a>
    
    </div>
  </div>
</template>
<script>
import { createPopper } from "@popperjs/core";

export default {
  data() {
    return {
      dropdownPopoverShow: false,
    };
  },
  mounted() {
  console.log("TableDropdown mounted");
  },

  methods: {
  toggleDropdown: function (event) {
    console.log('Dropdown toggle called'); // Check if the method is called
    event.preventDefault();
    this.dropdownPopoverShow = !this.dropdownPopoverShow; // Simplify the toggle logic
    console.log('Dropdown visibility:', this.dropdownPopoverShow); // Check the current state
    
    if (this.dropdownPopoverShow) {
      // Ensure the elements are correctly referenced
      console.log('Button reference:', this.$refs.btnDropdownRef);
      console.log('Popover reference:', this.$refs.popoverDropdownRef);
      
      createPopper(this.$refs.btnDropdownRef, this.$refs.popoverDropdownRef, {
        placement: "bottom-start",
      });
    }
  },
},

};
</script>
