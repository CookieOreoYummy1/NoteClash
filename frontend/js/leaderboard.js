 document.addEventListener('DOMContentLoaded', () => {
    function populateLeaderboard(data) {
        const leaderboardBody = document.getElementById('leaderboard-body');
        if (!leaderboardBody) return;
        leaderboardBody.innerHTML = '';


        const sortedData = data.sort((a, b) => b.total_rr - a.total_rr);

        sortedData.forEach((entry, index) => {
            const row = document.createElement('tr');

            const rank = index + 1;
            let rankDisplay;

            switch(rank) {
                case 1:
                    rankDisplay = '🥇';
                    break;
                case 2:
                    rankDisplay = '🥈';
                    break;
                case 3:
                    rankDisplay = '🥉';
                    break;
                default:
                    rankDisplay = rank;
            }

            const rankCell = document.createElement('td');
            rankCell.textContent = rankDisplay;

            const divisionCell = document.createElement('td');
            const divisionNameLower = entry.difficulty.toLowerCase();
            const divisionName = entry.difficulty.charAt(0).toUpperCase() + entry.difficulty.slice(1);

            const divisionBadge = document.createElement('span');
            divisionBadge.classList.add('division-badge');
            divisionBadge.classList.add(`division-${divisionNameLower}`);
            divisionBadge.textContent = divisionName;
            divisionCell.appendChild(divisionBadge);

            const userCell = document.createElement('td');
            userCell.textContent = entry.user;

            const rrCell = document.createElement('td');
            rrCell.textContent = Math.round(entry.total_rr).toLocaleString();

            row.appendChild(rankCell);
            row.appendChild(divisionCell);
            row.appendChild(userCell);
            row.appendChild(rrCell);

            leaderboardBody.appendChild(row);
    });
 }

async function fetchLeaderboard() {
    try {
        const response = await fetch('http://localhost:5000/leaderboard');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        populateLeaderboard(data);
    } catch (error) {
        console.error('Error fetching leaderboard data:', error);
        const leaderboardBody = document.getElementById('leaderboard-body');
        if (leaderboardBody) {
            leaderboardBody.innerHTML = '<tr><td colspan="4">Failed to load leaderboard data.</td></tr>';
        }
    }
}
fetchLeaderboard();
 })