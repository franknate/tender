<template>
  <div id="centerBox" class="d-flex flex-column">
    <h1 v-if="tender" class="text-center mt-2">
      Tender {{ tender.date }} {{ tender.market }} {{ tender.direction }}-{{ tender.tender_round }}
    </h1>
    <div class="container">
        <b-pagination
          v-model="currentRound"
          :total-rows="rows"
          :per-page="perPage"
          first-number
          last-number
          align="fill"
          class="my-3"
        ></b-pagination>
<!--       <div class="row bg-light border text-center">
          <div class="col-3 col-md-2"></div>
          <div class="col-3">
            <h3 v-if="currentRound > 1">Round {{ currentRound -1 }}</h3>
          </div>
          <div class="col-3">
            <h3>Round {{ currentRound }}</h3>
          </div>
          <div class="col-3">
              <h3 v-if="currentRound < 10">Round {{ currentRound + 1 }}</h3>
          </div>  
          <div class="col"></div>              
      </div> -->
      <div class="row border">
          <div class="col-3 col-md-2"></div>
          <div class="col-3 px-md-5">
            <span v-show="currentRound > 1">
              <label class="mb-0 py-1">price</label>
              <label class="mb-0 py-1 float-right">amount</label>
            </span>
          </div>
          <div class="col-3 px-md-5 bg-primary text-white">
              <label class="mb-0 py-1">price</label>
              <label class="mb-0 py-1 float-right">amount</label>
          </div>
          <div class="col-3 px-md-5">
            <span v-show="currentRound < 10">
              <label class="mb-0 py-1">price</label>
              <label class="mb-0 py-1 float-right">amount</label>
            </span>
          </div>
          <div class="col"></div>
      </div>
    </div>
    <div class="container rounded border-top border-bottom"
      v-if="tender"
      id="table"
    >
      <transition-group>
        <div
          v-for="unit in tender.units"
          :key="unit.id"
          class="row bg-light border mb-1"
        >
          <div class="d-flex justify-content-center col-3 col-md-2 align-items-center">
            {{ unit.fromdate | formatDate }} <br>
            {{ unit.todate | formatDate }}
          </div>
          <div class="col-3 px-md-5">
            <ul>
              <li v-for="bid in filterBids(unit, -1)" :key="bid.id">
                <span>
                  {{ bid.price }}
                </span>
                <span class="float-right pr-3">
                  {{ bid.amount }}
                </span>
              </li>
            </ul>
          </div>
          <div class="col-3 px-md-5 shadow-x">
            <ul>
              <li v-for="bid in filterBids(unit, 0)" :key="bid.id">
                <span>
                  {{ bid.price }}
                </span>
                <span class="float-right pr-3">
                  {{ bid.amount }}
                </span>
              </li>
            </ul>
          </div>
          <div class="col-3 px-md-5">
            <ul>
              <li v-for="bid in filterBids(unit, 1)" :key="bid.id">
                <span>
                  {{ bid.price }}
                </span>
                <span class="float-right pr-3">
                  {{ bid.amount }}
                </span>
              </li>
            </ul>
          </div>
          <div class="col"></div>
        </div>
      </transition-group>
    </div>
  </div>
</template>


<script>

export default {
  data() {
    return {
      tender: null,
      rows: 10,
      perPage: 1,
      currentRound: 1
    }
  },
  methods: {
    getResults() {
      fetch("http://127.0.0.1:8000/api/tenders/" + this.$store.state.currentTenderId, {
        method: "get"
      })
      .then((response) => {
        return response.json()
      })
      .then((jsonData) => {
        this.tender = jsonData
      })
    },
    filterBids(unit, shift) {
      return unit.bids.filter(bid => bid.bid_round == this.currentRound + shift)
    },
  },
  filters: {
    formatDate(date) {
      return new Date(date).toDateString().split(' ').slice(1).join(' ');
    }
  },
  created() {
    this.getResults()
    this.$store.subscribe(this.getResults)
  }
}

</script>


<style scoped>

ul {
  list-style-type: none;
  padding-left: 0px;
  margin-bottom: 0px;
}

#centerBox {
  height: 90vh;
}

#table {
  height: 100%;
  overflow: auto;
  scrollbar-width: thin;
}

.row {
  transition: all .7s;
}

.shadow-x {
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15);
  box-shadow: 12px 0 15px -4px rgba(0,0,0,.15), -12px 0 8px -4px rgba(0,0,0,.15);
}

</style>