<template>
  <div>
    <b-form inline>
      <b-form-datepicker v-model="date"></b-form-datepicker>
      <b-form-select v-model="market" :options="markets"></b-form-select>
      <b-form-select v-model="direction" :options="directions"></b-form-select>
      <b-form-select v-model="tender_round" :options="rounds"></b-form-select>
      <b-icon @click="clearFilters" icon="arrow-repeat" class="mx-2" id="clear-icon"></b-icon>
    </b-form>
    <transition-group name="tender-list" tag="b-list-group">
      <b-list-group-item
        v-for="tender in filteredTenders"
        :key="tender.id"
        class="d-flex text-monospace p-0 bg-secondary"
      >
        <b-button class="p-2 flex-grow-1" @click="switchTender(tender.id)">
          Tender {{ tender.datestr }} {{ tender.market }}
          <b-icon :icon="arrowIcon(tender.direction)" :variant="arrowVariant(tender.direction)">
          </b-icon>{{ tender.tender_round }}
        </b-button>
        <b-button
          :id="'delete-' + tender.id"
          class="p-2"
        >
          <b-icon icon="trash"></b-icon>
        </b-button>
        <b-popover
          :target="'delete-' + tender.id"
          triggers="click"
          placement="top"
        >
          <template #title>Are you sure?</template>
          <b-button
            variant="danger"
            @click="deleteTender(tender.id)"
            class="m-1"
          >
            Delete
          </b-button>
          <b-button
            variant="light"
            @click="onClose"
            class="m-1"
          >
            Cancel
          </b-button>
        </b-popover>
      </b-list-group-item>
    </transition-group>
  </div>
</template>

<script>
export default {
  data() {
    return {
      date: null,
      market: null,
      direction: null,
      tender_round: null,
      markets: [
        { value: null, text: "Market" },
        { value: "aFRR", text: "aFRR" },
        { value: "mFRR", text: "mFRR" }
      ],
      directions: [
        { value: null, text: "Direction" },
        { value: "U", text: "Up" },
        { value: "D", text: "Down" }
      ],
      rounds: [
        { value: null, text: "Round" },
        { value: 1, text: "1" },
        { value: 2, text: "2" }
      ]
    };
  },
  methods: {
    clearFilters() {
      this.date = null,
      this.market = null,
      this.direction = null,
      this.tender_round = null
    },
    switchTender(tenderId) {
      this.$store.dispatch("switchTender", tenderId)
    },
    deleteTender(tenderId) {
      this.$store.dispatch("deleteTender", tenderId)
    },
    onClose() {
      this.$root.$emit('bv::hide::popover')
    },
    arrowIcon(direction) {
      return direction == "U" ? "caret-up-fill" : "caret-down-fill"
    },
    arrowVariant(direction) {
      return direction == "U" ? "success" : "danger"
    }
  },
  computed: {
    tenders() {
      return this.$store.getters.Tenders 
    },
    filteredTenders() {
      return this.tenders.filter(tender =>
        (this.date == null || this.date == tender.date) &&
        (this.market == null || this.market == tender.market) &&
        (this.direction == null || this.direction == tender.direction) &&
        (this.tender_round == null || this.tender_round == tender.tender_round)
      ).slice(0,8)
    }
  },
  created() {
    this.$store.dispatch("getTenders");
  }
};
</script>

<style scoped>

.list-group {
  text-align: left;
  margin-top: 20px;
}
.list-group-item {
  margin-bottom: 2px;
  transition: all .7s;
}
#clear-icon {
  color: grey;
}
#clear-icon:hover {
  color: darkslategrey;
  cursor: pointer;
}
.tender-list-enter,
.tender-list-leave-to {
  max-height: 0px;
  padding-top: 0px !important;
  padding-bottom: 0px !important;
  overflow: hidden;
}
.tender-list-enter-to,
.tender-list-leave {
  max-height: 80px;
}

</style>
