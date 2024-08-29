<template>
  <div class="pages-container flex flex-col gap-8">
    <section class="table-section">

      <inventory-page />
    </section>
    <section class="table-section">
      <menu-page />
    </section>
    <section class="table-section">
      <user-page />
    </section>
  </div>
</template>

<script>
import InventoryPage from './InventoryPage.vue';
import MenuPage from './MenuPage.vue';
import UserPage from './UserPage.vue';

export default {
  components: {
    InventoryPage,
    MenuPage,
    UserPage
  }
};
</script>

<style>
.pages-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
