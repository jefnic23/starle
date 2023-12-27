import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type { Starle } from '../types/starle.type';

export const starles: Writable<Starle[]> = writable([]);
export const currentStarle: Writable<Starle> = writable();
