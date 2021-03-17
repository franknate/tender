<template>
  <b-table-simple
    v-if="currentTender"
    sticky-header="100%"
    dark
    hover
  >
    <b-thead>
      <b-tr class="text-center">
        <b-th scope="col" style="width: 25%">
          <b-button
            type="submit"
            variant="success"
            @click="makeBid"
          >Make Bid</b-button>
        </b-th>
        <b-th scope="col" style="width: 25%">5MW</b-th>
        <b-th scope="col" style="width: 25%">10MW</b-th>
        <b-th scope="col" style="width: 25%">15MW</b-th>
      </b-tr>
    </b-thead>
    <b-tbody>
      <b-tr
        v-for="(unit, index) in currentTender.units"
        :key="unit.id"
      >
        <b-th scope="row">
          {{ formatDate(unit.fromdate) }} <br>
          {{ formatDate(unit.todate) }}
        </b-th>
        <b-td>
          <b-form-input
            v-model="bids[index]['5']"
            type="number"
          ></b-form-input>
        </b-td>
        <b-td>
          <b-form-input
            v-model="bids[index]['10']"
            type="number"
          ></b-form-input>
        </b-td>
        <b-td>
          <b-form-input
            v-model="bids[index]['15']"
            type="number"
          ></b-form-input>
        </b-td>
      </b-tr>
    </b-tbody>
  </b-table-simple>
</template>

<script>
export default {
  data() {
    return {
      makeBidError: null
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toDateString().split(' ').slice(1).join(' ');
    },
    makeBid() {
      const Bid = {
        tender_id: this.currentTender.id,
        round: this.$store.state.lastRound,
        bids: this.bids
      }
      this.currentTender.id
      fetch(this.$store.state.BASE_URL + "bid/", {
        method: "POST",
        headers: {
          "Authorization": "Token " + this.$store.getters.Token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(Bid)
      })
      .then(response => response.blob())
      .then(blob => {
        var file = window.URL.createObjectURL(blob);
        window.location.assign(file);
      })
    }
  },
  computed: {
    currentTender() {
      return this.$store.state.currentTender;
    },
    currentRound() {
      return this.$store.state.currentRound;
    },
    bids() {
      let initialBids = {}
      for (let i = 0; i < this.currentTender.units.length; i++) {
        let day = new Date(this.currentTender.units[i].fromdate).getDay()
        let isWeekend = (day === 6) || (day === 0);
        let bid_round = this.currentTender.bid_rounds[this.$store.state.lastRound-1]
        let max_price = isWeekend ? bid_round.max_price_wkdy : bid_round.max_price_wknd
        initialBids[i] = {
          "5": max_price,
          "10": max_price,
          "15": max_price
        }
      }
      return initialBids;
    }
  }
}
</script>

<style>

</style>