<template>
  <div class="min-h-screen bg-gradient-to-b from-sky-50 via-white to-emerald-50 flex flex-col items-center px-4 py-10">
    <h1 class="mb-2 text-4xl font-extrabold text-emerald-700 tracking-tight">
      📣 La Gazette locale 
    </h1>
    <p class="mb-8 text-gray-600 text-center">
      De la graine 🌱 au grand arbre 🌳 : suivez la progression des équipes.
    </p>

    <div class="w-full max-w-4xl bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg border border-emerald-100 overflow-hidden">
      <!-- Header de la carte -->
      <div class="flex items-center justify-between px-6 py-4 border-b bg-gradient-to-r from-emerald-50 to-sky-50">
        <div>
          <h2 class="text-lg font-semibold text-gray-800">Podium des équipes</h2>
          <p class="text-sm text-gray-500">Classement mis à jour en temps réel pendant la NDI.</p>
        </div>
        <span class="inline-flex items-center gap-1 px-3 py-1 text-xs font-medium rounded-full bg-emerald-100 text-emerald-700">
          🌳 Arbre &nbsp;•&nbsp; 🌱 Pousse &nbsp;•&nbsp; 🫘 Graine
        </span>
      </div>

      <table class="w-full text-left border-collapse">
        <thead class="bg-gray-50">
          <tr class="text-sm text-gray-500">
            <th class="p-4 font-semibold border-b">Rang</th>
            <th class="p-4 font-semibold border-b">Village🏘️</th>
            <th class="p-4 font-semibold border-b">CO2 réduits🍃</th>
            <th class="p-4 font-semibold border-b">Quêtes accomplies🗺️</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="(team, index) in ranking"
            :key="team.id"
            :class="[
              'border-b last:border-b-0 transition-colors',
              index === 0
                ? 'bg-emerald-50/80 hover:bg-emerald-100/80'
                : index === 1
                ? 'bg-lime-50/80 hover:bg-lime-100/80'
                : index === 2
                ? 'bg-amber-50/60 hover:bg-amber-100/70'
                : 'odd:bg-white even:bg-gray-50 hover:bg-gray-100'
            ]"
          >
            <!-- Rang -->
            <td class="p-4">
              <div class="flex items-center gap-3">
                <div
                  class="w-9 h-9 flex items-center justify-center rounded-full text-xl"
                  :class="{
                    'bg-emerald-600 text-white shadow-sm': index === 0,
                    'bg-lime-500 text-white shadow-sm': index === 1,
                    'bg-amber-500 text-white shadow-sm': index === 2,
                    'bg-gray-100 text-gray-700': index > 2
                  }"
                >
                  <span v-if="index === 0" aria-label="Premier rang">🌳</span>
                  <span v-else-if="index === 1" aria-label="Deuxième rang">🌱</span>
                  <span v-else-if="index === 2" aria-label="Troisième rang">🫘</span>
                  <span v-else class="text-sm font-semibold">#{{ index + 1 }}</span>
                </div>
              </div>
            </td>

            <!-- Nom équipe -->
            <td class="p-4 text-gray-800 font-medium">
              {{ team.name }}
            </td>

            <!-- Points -->
            <td class="p-4">
              <span class="text-base font-extrabold text-emerald-700">
                {{ team.points }} kg CO₂-eq
              </span>
            </td>

            <!-- Défis validés -->
            <td class="p-4">
              <span class="inline-flex items-center px-2.5 py-1 text-xs font-semibold rounded-full bg-sky-100 text-sky-700">
                {{ team.completedChallenges }} validés
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const ranking = [
  { id: 1, name: 'Les Chili Peppers', points: 1250, completedChallenges: 15 },
  { id: 2, name: 'Code Warriors', points: 1100, completedChallenges: 13 },
  { id: 3, name: 'Dev Titans', points: 950, completedChallenges: 11 },
  { id: 4, name: 'Null Pointers', points: 800, completedChallenges: 9 },
  { id: 5, name: 'Syntax Errors', points: 650, completedChallenges: 7 },
  { id: 6, name: 'Infinite Loops', points: 500, completedChallenges: 6 },
  { id: 7, name: 'Git Masters', points: 450, completedChallenges: 5 },
  { id: 8, name: 'Vue Vixens', points: 300, completedChallenges: 3 },
]
</script>
