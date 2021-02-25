<template>
  <div>
    <b-form inline>
      <b-form-datepicker v-model="date"></b-form-datepicker>
      <b-form-select v-model="market" :options="markets"></b-form-select>
      <b-form-select v-model="direction" :options="directions"></b-form-select>
      <b-form-select v-model="tender_round" :options="rounds"></b-form-select>
      <b-icon @click="clearFilters" icon="arrow-repeat" class="mx-2" id="clear-icon"></b-icon>
    </b-form>
    <b-list-group>
      <b-list-group-item v-for="tender in filteredTenders" :key="tender.id" class="text-monospace">
        Tender {{ tender.date }} {{ tender.market }}
        <b-icon :icon="tender.arrowIcon" :variant="tender.arrowColor"></b-icon>{{ tender.tender_round }}
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tenders: [],
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
    getTenders() {
      fetch("http://127.0.0.1:8000/api/tenders/", {
        method: "get"
      })
      .then((response) => {
        return response.json()
      })
      .then((jsonData) => {
        this.tenders = jsonData
        this.addArrowIcons()
      })
    },
    clearFilters() {
      this.date = null,
      this.market = null,
      this.direction = null,
      this.tender_round = null
    },
    addArrowIcons() {
      for (var tender of this.tenders) {
        tender.arrowIcon = tender.direction == "U" ? "caret-up-fill" : "caret-down-fill";
        tender.arrowColor = tender.direction == "U" ? "success" : "danger";
      }
    }
  },
  computed: {
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
    this.getTenders();
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
}

#clear-icon {
  color: grey;
}

#clear-icon:hover {
  color: darkslategrey;
  cursor: pointer;
}

</style>
