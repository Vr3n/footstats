db = db.getSiblingDB('footstats')

db.createUser({
  user: 'vr3n',
  pwd: 'footyxg',
  roles: [
    {
      role: 'dbOwner',
      db: 'footstats' 
    }
  ]
})


// drop existing continents if exists.
db.continents.drop()


// Create 'continents' collection and insert documents.
const continents = [
  { "name": "Asia" },
  { "name": "Europe" },
  { "name": "Africa" },
  { "name": "North America" },
  { "name": "South America" },
  { "name": "Australia" },
  { "name": "Antarctica" }
];
