<template>
  <div>
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
      <b-tbody v-if="bids">
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
              v-model.number="bids[index][5]"
              :disabled="!bids[index][5]"
              :class="{ 'text-danger': isOut(index, 5) }"
              type="number"
            ></b-form-input>
          </b-td>
          <b-td>
            <b-form-input
              v-model.number="bids[index][10]"
              :disabled="!bids[index][10]"
              :class="{ 'text-danger': isOut(index, 10) }"
              type="number"
            ></b-form-input>
          </b-td>
          <b-td>
            <b-form-input
              v-model.number="bids[index][15]"
              :disabled="!bids[index][15]"
              :class="{ 'text-danger': isOut(index, 15) }"
              type="number"
            ></b-form-input>
          </b-td>
        </b-tr>
      </b-tbody>
    </b-table-simple>
    <b-alert
      v-model="showMakeBidError"
      variant="danger"
      fade
    >
      <b>Upload Falied!</b>
    </b-alert>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bids: null,
      initialBids: null,
      showMakeBidError: false
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toDateString().split(' ').slice(1).join(' ');
    },
    getBids() {
      fetch(this.$store.state.BASE_URL + "bid/" + this.currentTender.id + "/", {
        method: "GET",
        headers: {
          "Authorization": "Token " + this.$store.getters.Token,
        }
      })
      .then(response => response.json().then(data => ({status: response.status, body: data})))
      .then(response => {
        if (response.status == "200") {
          this.bids = response.body
          this.initialBids = JSON.parse(JSON.stringify(response.body))
        } else {
          console.error("Error in BidTable.vue, getBids()")
        }
      });
    },
    makeBid() {
      for (var i = 0; i < this.bids.length; i++) {
        if (this.isOut(i, 5)) this.bids[i][5] = 0 
        if (this.isOut(i, 10)) this.bids[i][10] = 0 
        if (this.isOut(i, 15)) this.bids[i][15] = 0
      }
      fetch(this.$store.state.BASE_URL + "bid/" + this.currentTender.id + "/", {
        method: "POST",
        headers: {
          "Authorization": "Token " + this.$store.getters.Token,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.bids)
      })
      .then(response => response.blob().then(data => ({ok: response.ok, body: data})))
      .then(response => {
        if (response.ok) {
          this.showMakeBidError = false
          this.downloadFile(response.body)
        } else {
          this.showMakeBidError = true
        }
      });
    },
    downloadFile(blob) {
      var url = window.URL.createObjectURL(blob)
      var a = document.createElement("a")
      document.body.appendChild(a)
      a.style = "display: none"
      a.href=url
      a.download = `${this.currentTender.datestr}_${this.currentTender.market}_${this.currentTender.direction}_${this.currentTender.tender_round}_${this.currentTender.current_bid_round}.xlsx`
      a.click()
      window.URL.revokeObjectURL(url)
    },
    isOut(index, amount) {
      return this.bids[index][amount] > this.initialBids[index][amount]
    }
  },
  computed: {
    currentTender() {
      return this.$store.state.currentTender;
    },
    currentRound() {
      return this.currentTender.current_bid_round;
    }
  },
  watch: {
    currentTender(newRound, oldRound) {
      this.getBids()
    }
  }
}
</script>

<style>

</style>