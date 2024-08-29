<template>
  <div class="bg-primary w-screen m-auto h-screen flex justify-center items-center">

    <div class="w-full md:w-1/2 lg:w-1/4 px-4">
      <div class="relative flex flex-col break-words min-w-full shadow-lg rounded-lg bg-blueGray-200 border-0">
        <div class="rounded-t mb-0 px-6 py-6">
          <div class="text-center mb-3">
            <h6 class="text-black text-sm font-bold">
              Log in or Register with
            </h6>
          </div>
          <hr class="border-b-1 border-blueGray-300" />

          <div class="w-36 m-auto pt-6 pb-6">
            <button @click='login'
              class="gap-4 w-full text-center bg-white active:bg-blueGray-50 text-blueGray-700 m-auto px-4 py-2 rounded outline-none focus:outline-none shadow hover:shadow-md inline-flex items-center ease-linear transition-all duration-150"
              type="button">
              <img alt="..." :src="googleLogo" />
              Google
            </button>
          </div>
          <hr class="border-b-1 border-blueGray-300" />

          <div>
            <p class="text-center text-sm text-black">By signing in, you agree to Rev's terms of service and privacy
              policy.</p>
          </div>
          <!-- <hr class="mt-6 border-b-1 border-blueGray-300" /> -->
        </div>

      </div>

    </div>

  </div>
</template>
<script>
import googleLogo from "@/assets/google.svg";
import { googleSdkLoaded } from "vue3-google-login";
import axios from "axios";
import { setCookie } from "../../cookies/cookies";
import { PROD_BASE_URL } from "../../main";

export default {
  data() {
    return {
      user: null,
      googleLogo
    };
  },
  methods: {
    login() {
      googleSdkLoaded(google => {
        const intendedRoute = this.$route.query.redirect || "/";
        google.accounts.oauth2
          .initCodeClient({
            client_id:
              "702708192712-sa1viksf6nsfbkb5h711it18n0g6sse9.apps.googleusercontent.com",
            scope: "email profile openid",
            callback: response => {
              if (response.code) {
                this.updateBackendUser(response.code, (dbUserData) => {
                  this.$router.replace(intendedRoute);
                });

              }
            }
          })
          .requestCode();
      });
    },
    async updateBackendUser(code, successCallback, failCallback) {
      try {
        const response = await axios.post(
          "https://oauth2.googleapis.com/token",
          {
            code,
            client_id:
              "702708192712-sa1viksf6nsfbkb5h711it18n0g6sse9.apps.googleusercontent.com",
            client_secret: "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",
            redirect_uri: "postmessage",
            grant_type: "authorization_code"
          }
        );
        console.log(response.data)
        const accessToken = response.data.access_token;
        // Fetch user details using the access token
        const userResponse = await axios.get(
          "https://www.googleapis.com/oauth2/v3/userinfo",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`
            }
          }
        );

        if (userResponse && userResponse.data) {
          const { email, given_name: name} = userResponse.data;
          this.user = userResponse.data;
          setCookie("email", email, 10);
          setCookie("name", name, 10);
          const userData = { email, name }
          const dbUserData = await axios.post(`${PROD_BASE_URL}/user/`, userData);
          setCookie("id", dbUserData.data.id, 10);

          // if (dbUserData.data.points !== null && dbUserData.data.points !== undefined) {
          //   setCookie("points", dbUserData.data.points, 10);
          // } else {
          //   // Default points value if not available
          //   setCookie("points", 0, 10);
          // }

          successCallback(dbUserData.data)
        }
        else {
          // Handle the case where userResponse or userResponse.data is undefined
          console.error("Failed to fetch user details.");
          failCallback()
        }

      } catch (error) {
        console.error("Failed to send authorization code:", error);
      }
    }
  }
};

</script>
