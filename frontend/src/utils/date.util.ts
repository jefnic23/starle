export function getDateSeed(): number {
    const today = new Date()
    const year = today.getFullYear();
    const month = today.getMonth();
    const day = today.getDay();

    return parseInt(`${year}${month}${day}`);
}