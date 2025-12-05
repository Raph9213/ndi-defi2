<template>
  <div class="bg-white rounded-3xl shadow-lg border border-gray-100 flex flex-col lg:flex-row relative lg:col-span-2 overflow-hidden">
    <!-- Tribe Info -->
    <div class="p-8 flex flex-col justify-between relative lg:w-1/2 border-b lg:border-b-0 lg:border-r border-gray-100">
      <div class="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-indigo-50 rounded-full blur-xl opacity-50"></div>
      
      <div>
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          Ma Tribu
        </h2>
        
        <div class="space-y-6">
          <div>
            <p class="text-sm text-gray-500 uppercase tracking-wider font-semibold">Nom de la tribu</p>
            <p class="text-2xl font-bold text-green-600 mt-1">{{ customVillage.name }}</p>
          </div>
          
          <div>
            <p class="text-sm text-gray-500 uppercase tracking-wider font-semibold">Score Total</p>
            <p class="text-4xl font-black text-green-600 mt-1">{{ getTotalScore() }} g <span class="text-sm font-medium text-gray-500">de CO2 évité</span></p>
          </div>
        </div>
      </div>

      <div class="mt-8 pt-6 border-t border-gray-100" @click="copyLink()">
        <p class="text-sm text-gray-500 mb-2">Code d'invitation secret</p>
        <div class="flex items-center gap-2 bg-gray-50 p-3 rounded-xl border border-gray-200 group cursor-pointer hover:bg-gray-100 transition-colors">
          <code class="text-lg font-mono font-bold text-gray-700 flex-1">{{ customVillage.inviteLink }}</code>
          <svg class="w-5 h-5 text-gray-400 group-hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
        </div>
      </div>
    </div>

    <!-- Leaderboard -->
    <div class="p-8 lg:w-1/2 bg-gray-50/50">
      <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <svg class="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
        Les meilleurs compagnons
      </h2>
      
      <div class="overflow-y-auto max-h-72 pr-2 custom-scrollbar">
        <ul class="space-y-3">
          <li v-for="(member, index) in customVillage.members" :key="member.name" 
              class="flex items-center justify-between p-3 rounded-xl transition-all hover:bg-white border border-transparent hover:border-gray-200 hover:shadow-sm">
            <div class="flex items-center gap-3">
              <div class="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full font-bold text-xs"
                   :class="{
                     'bg-yellow-100 text-yellow-700': index === 0,
                     'bg-gray-100 text-gray-700': index === 1,
                     'bg-orange-100 text-orange-800': index === 2,
                     'bg-gray-200 text-gray-500': index > 2
                   }">
                {{ index + 1 }}
              </div>
              <div class="flex items-center gap-2">
                <span class="font-semibold text-gray-900 text-sm">{{ member.name }}</span>
              </div>
            </div>
            <div class="font-bold text-gray-900 text-sm">
              {{ member.score.toLocaleString() }} g
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  customVillage: {
    name: string;
    teamScore: number;
    members: Array<{
      name: string;
      avatar: string;
      score: number;
    }>;
    inviteLink: string;
  }
}>();

const getTotalScore = () => {
    return props.customVillage.members.reduce((total, member) => total + member.score, 0);
}
function copyLink() {
    navigator.clipboard.writeText(props.customVillage.inviteLink);
}
</script>
