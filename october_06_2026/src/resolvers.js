const artists = [
  { id: 1, name: 'Duki', genre: 'Trap' },
  { id: 2, name: 'The Offspring', genre: 'Punk Rock' },
  { id: 3, name: 'La Vela Puerca', genre: 'Rock Uruguayo' },
  { id: 4, name: 'Fito Páez', genre: 'Rock Nacional' },
  { id: 5, name: 'Taylor Swift', genre: 'Pop' },
];

const concerts = [
  { id: 1, artistId: 1, date: '2025-10-05', venue: 'Estadio Monumental' },
  { id: 2, artistId: 2, date: '2025-10-15', venue: 'Madison Square Garden' },
  { id: 3, artistId: 3, date: '2025-10-25', venue: 'Velódromo Municipal' },
  { id: 4, artistId: 4, date: '2025-11-05', venue: 'Movistar Arena' },
  { id: 5, artistId: 5, date: '2025-11-20', venue: 'Wembley Stadium' },
];

  
  const resolvers = {
    Query: {
      artists: () => artists,
      concerts: () => concerts.map(concert => ({
        ...concert,
        artist: artists.find(artist => artist.id === concert.artistId),
      })),
    },
  };
  
  module.exports = resolvers;