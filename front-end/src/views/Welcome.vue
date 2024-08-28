<template>
  <div class="w-screen min-h-screen bg-primary">
    <div id="google_translate_element" />
    <div class="fixed right-0 text-white font-semibold p-2">
      <ul class="divide-x-2 flex">
        <li @click="logout()" class="px-2 hover:underline cursor-pointer" v-if="userName != ''" tabindex="0">
          Log Out
        </li>
        <li v-else class="px-2"><a href="/auth">Log In</a></li>
      </ul>
    </div>
    <div class="min-h-screen flex flex-col justify-center items-center gap-3">
      <div><img :src=image alt="Rev's logo"></div>
      <h1 v-if="userName != ''" class="text-white font-semibold text-4xl mb-4">Welcome, {{ userName }}!</h1>
      <h1 v-else class="text-white font-semibold text-4xl mb-4">Welcome!</h1>
      <div class=" grid gap-8 grid-cols-1 md:grid-cols-2">
        <Button @click="navigateTo('/menu-board')">Menu Board</Button>
        <Button v-show="userStatus >= 2" @click="navigateTo('/cashier-order')">Cashier Order</Button>
        <Button v-show="userStatus >= 3" @click="navigateTo('/manager')">Manager</Button>
        <Button @click="navigateTo('/customer-order')">Customer Order</Button>
      </div>
    </div>
  </div>
</template>

<script>
import logo from "@/assets/revs_logo.png";
import Button from "@/components/Buttons/PrimaryButton.vue"
import { clearAllCookies, getCookie } from "../cookies/cookies";
import { googleLogout } from 'vue3-google-login'
import axios from 'axios';
import { PROD_BASE_URL } from "../main";

export default {
  components: {
    Button
  },

  methods: {
    navigateExternal(route) {
      window.open(route, '_blank')
    },
    navigateTo(route) {
      this.$router.push(route)
    },
    async loadUser() {

      const userData = await axios.get(`${PROD_BASE_URL}/user/${getCookie("id")}`)

      this.userStatus = userData.data.user_type;
    },
    logout() {
      googleLogout();
      clearAllCookies();
      location.reload()
    }
  },
  name: 'TranslateWidget',
  mounted() {
    this.userName = getCookie("name");
    this.userId = getCookie("id")
    if (this.userId != "") {
      this.loadUser()
    }
    let googleTranslateScript = document.createElement('script');
    googleTranslateScript.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    googleTranslateScript.async = true;
    document.body.appendChild(googleTranslateScript);

    window.googleTranslateElementInit = function () {
      new window.google.translate.TranslateElement({ pageLanguage: 'en', gaTrack: false }, 'google_translate_element');
    };

  },
  data() {
    return {
      image: logo,
      userName: "",
      userId: -1,
      userStatus: 0, //customer
    };
  },
};
</script>

<style>
#goog-gt-tt {
  display: none !important;
  top: 0px !important;
}

/* #google_translate_element .goog-te-gadget {color:#fff} */
/*#google_translate_element .goog-te-gadget a {
  color: #fff
}*/

#google_translate_element .goog-te-gadget {
  font-size: 16px;
}

#google_translate_element .goog-te-gadget a {
  font-size: 16px;
}

.VIpgJd-ZVi9od-aZ2wEe-wOHMyf-ti6hGc {
  display: none;
}

.skiptranslate>iframe {
  visibility: none !important;
  display: none !important;
}

.goog-te-gadget {
  position: fixed;
  top: -10px;
}


body {
  background-color: #580726;
}
</style>
