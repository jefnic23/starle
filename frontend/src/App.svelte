<script lang="ts">
	import { getAsync } from "./utils/http.util"
	import { getDateSeed } from "./utils/date.util";
    import { starles, names } from "./stores/game.store";
	import Game from "./components/Game.svelte";
	import type { Starle } from "./types/starle.type";
	import { fade } from "svelte/transition";

	const loadData = async (): Promise<void> => {
		// todo: save data to localStorage and prevent multiple api calls
		let starles_data = await getAsync<Starle[]>(`/api/starle?seed=${getDateSeed()}`);
		$starles = starles_data;

		let names_data = await getAsync<string[]>('/api/names');
		$names = names_data;
	}
</script>

<main>
	{#await loadData()}
		<div class="loading-screen" in:fade={{ duration: 377 }}>
			Loading...
		</div>
	{:then} 
		<div class="game-container" in:fade={{ duration: 377 }}>
			<Game />
		</div>
	{/await}
</main>

<style>
	.loading-screen {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        font-size: 2em;
    }
</style>
