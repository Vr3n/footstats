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
