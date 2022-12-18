<template>
  <div>
    <b-img class="img-size" center :src="imagepath" alt="Center image"></b-img>
    <p class="mt-4 mb-1 p-0"><b>Reasoning:</b></p>
    <b-input-group v-for="(input, k) in item.reasoning" :key="`reasoning-${k}`">
      <b-form-textarea
        id="reasoning-input"
        v-model="input.reasoning"
        placeholder="Enter reasonings"
        rows="2"
        max-rows="3"
      ></b-form-textarea>
      <b-input-group-append>
        <span>
          <i @click="remove(k)" v-show="k || (!k && item.reasoning.length > 1)"
            >Remove</i
          >
          <i @click="add(k)" v-show="k == item.reasoning.length - 1"
            >Add fields</i
          >
        </span>
      </b-input-group-append>
    </b-input-group>

    <p v-if="errorNum != 0" class="error mt-0 pt-0">
      Reasoning {{ errorNum }} is either empty or does not contain the social
      target.
    </p>

    <p class="mt-4 mb-1 p-0"><b>Remarks:</b></p>
    <b-input-group>
      <b-form-textarea
        id="remarks-input"
        v-model="item.remarks"
        placeholder="Enter remarks (e.g. this meme seems to be attacking the 'politics' more than 'females')"
        rows="2"
        max-rows="3"
      ></b-form-textarea>
    </b-input-group>

    <p class="mt-4 mb-1 p-0"><b>Additional:</b></p>
    <b-input-group>
      <b-form-textarea
        id="additional-input"
        v-model="item.additional"
        placeholder="Enter additional information (e.g. the idea of 'smoke -> native america making peace' comes from their culture where they smoke peace pipe to make peace treaty). Feel free to include links as well"
        rows="3"
        max-rows="3"
      ></b-form-textarea>
    </b-input-group>

    <div class="mt-2" style="text-align: center">
      <b-button variant="primary" @click="onSaveButton()">Submit</b-button>
    </div>
  </div>
</template>

<script>
import { Settings } from "../config/api.config";
import auth from "../utils/auth";
import axios from "axios";
import moment from "moment-timezone";

export default {
  name: "explanation",
  props: ["item", "targets", "itemLoaded"],
  data() {
    return {
      // inputs: this.,
      errorNum: 0,
    };
  },
  computed: {
    imagepath: function () {
      return `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/${this.item.Meme.image}`;
    },
    lTargets: function() {
      return this.targets.map((f) => {
        return f.toLowerCase();
      })
    }
  },
  methods: {
    add() {
      this.item.reasoning.push({
        reasoning: "",
      });
    },

    remove(index) {
      this.item.reasoning.splice(index, 1);
    },
    async onSaveButton() {
      // Check for errors
      this.errorNum = 0;
      for (let i = 0; i < this.item.reasoning.length; i++) {
        const element = this.item.reasoning[i];

        if (element.reasoning === "" || element.reasoning === null) {
          this.errorNum = i + 1;
          break;
        }

        var containTarget = false;
        var reasoning = element.reasoning.toLowerCase();
        for (let k = 0; k < this.lTargets.length; k++) {
          const target = this.lTargets[k];

          if (reasoning.includes(target)) {
            containTarget = true;
            break;
          }
        }

        if (!containTarget) {
          this.errorNum = i + 1;
        }
      }

      if (this.errorNum != 0) return;

      const body = new URLSearchParams({
        id: this.item.id,
        reasoning: JSON.stringify(this.item.reasoning),
        remarks: this.item.remarks,
        additional: this.item.additional,
      });

      const config = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "x-access-token": auth.getToken(),
        },
      };

      const res = await axios
        .post(
          `${Settings.PROTOCOL}://${Settings.HOST}:${Settings.PORT}/api/memes/explanation`,
          body.toString(),
          config
        )
        .catch((error) => {
          console.log(error);
        });

      if (res.status === 200) {
        this.item.updatedAt = moment().utc().format();
        this.$emit("onSaveClick");
      }
    },
  },
};
</script>

<style>
.img-size {
  max-width: 100%;
  max-height: 70vh;
}
</style>