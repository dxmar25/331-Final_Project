<template>
  <button :class="classes"
    class="shadow-lg hover:opacity-85 flex items-center bg-primary text-white rounded-md border-2 !focus-visible:border-green-50">
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    size: {
      type: String,
      default: 'medium'
    },
    class: {
      type: String
    },
  },
  computed: {
    classes() {
      return [
        `btn-${this.size}`,
        this.class
      ];
    }
  },
}
</script>
<style>
.btn-small {
  padding: 6px 12px;
  font-size: 20px;
}

.btn-medium {
  padding: 6px 15px;
  font-size: 24px;

}

.btn-large {
  padding: 17px 25px;
  font-size: 45px;

}
</style>