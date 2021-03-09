<template>
  <b-table-simple
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
        v-for="unit in currentTender.units"
        :key="unit.id"
      >
        <b-th scope="row">
          {{ formatDate(unit.fromdate) }} <br>
          {{ formatDate(unit.todate) }}
        </b-th>
        <b-td>
          <b-form-input
            v-model="bids[unit.id]['5']"
            type="number"
          ></b-form-input>
        </b-td>
        <b-td>
          <b-form-input
            v-model="bids[unit.id]['10']"
            type="number"
          ></b-form-input>
        </b-td>
        <b-td>
          <b-form-input
            v-model="bids[unit.id]['15']"
            type="number"
          ></b-form-input>
        </b-td>
      </b-tr>
    </b-tbody>
  </b-table-simple>
</template>

<script>
export default {
  methods: {
    formatDate(date) {
      return new Date(date).toDateString().split(' ').slice(1).join(' ');
    },
    makeBid() {
      console.log("Bids:", this.bids)
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
      for (let unit of this.currentTender.units) {
        initialBids[unit.id] = {
          "5": 0,
          "10": 0,
          "15": 0
        }
      }
      return initialBids;
    }
  }
}
</script>

<style>

</style>