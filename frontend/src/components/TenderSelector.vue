<template>
  <b-jumbotron
    header="Select a Tender"
    header-level="4"
    lead="Filter the tenders with the selectors below"
  >
    <b-form inline>
      <b-form-datepicker v-model="date"></b-form-datepicker>
      <b-form-select v-model="market" :options="markets"></b-form-select>
      <b-form-select v-model="direction" :options="directions"></b-form-select>
      <b-form-select v-model="tender_round" :options="rounds"></b-form-select>
    </b-form>
    <b-list-group>
      <b-list-group-item v-for="tender in filteredTenders" :key="tender.id">
        Tender - {{ tender.date }} {{ tender.market }} {{ tender.direction}}-{{ tender.tender_round }}
      </b-list-group-item>
    </b-list-group>
  </b-jumbotron>
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
        { value: null, text: "Filter market" },
        { value: "aFRR", text: "aFRR" },
        { value: "mFRR", text: "mFRR" }
      ],
      directions: [
        { value: null, text: "Filter direction" },
        { value: "U", text: "Up" },
        { value: "D", text: "Down" }
      ],
      rounds: [
        { value: null, text: "Filter round" },
        { value: 1, text: "1" },
        { value: 2, text: "2" }
      ]
    };
  },
  methods: {
    getTenders() {
      fetch("http://127.0.0.1:8000/api/tenders", {
        method: "get"
      })
      .then((response) => {
        return response.json()
      })
      .then((jsonData) => {
        this.tenders = jsonData
      })
    }
  },
  computed: {
    filteredTenders() {
      return this.tenders.filter(tender =>
        (this.date == null || this.date == tender.date) &&
        (this.market == null || this.market == tender.market) &&
        (this.direction == null || this.direction == tender.direction) &&
        (this.tender_round == null || this.tender_round == tender.tender_round)
      )
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

</style>
