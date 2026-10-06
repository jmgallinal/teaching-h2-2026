const { gql } = require('apollo-server');

const typeDefs = gql`
  type Artist {
    id: ID
    name: String
    genre: String
  }

  type Concert {
    id: ID
    artist: Artist
    date: String
    venue: String
  }

  type Query {
    artists: [Artist]
    concerts: [Concert]
  }
`;

module.exports = typeDefs;