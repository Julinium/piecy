# SCRATCHPAD
This file is just about anything that comes by and may be thought of later.  
It's not a formal tasks list.

### Loyalty programs
Implement loyalty cards, discount points, ...

### Special prices per products
Products have a price per channel.  

### Special discounts 
Make special discounts per client or per client category.

### Barcode and QR codes
Each product has a barcode and probably a QR code.  
Bar codes can be scanned to edit Purchase orders reception and Sales orders.

### Price tags printing
Let the user edit and print price tags to hang on physical products.  
Tags include barcode, price, name and eventually other data.

### Stock reservation
When a sales order is created, reserve the quantity.  
User may also reserve stock without a sales order ? This is not needed, the user can create a draft sales order for the stock to be reserved.

### Restocking policies
Make minimal safe stocks per channel.  
Send notification and/or make a purchase order when past the safe stock level.

### Stock inventory breakdown
Make visible: How many items are available, how many are reserved ?

### Negative stock orders ?
Let user decide whether to allow orders even if the available quantity is not enough and mark the order as waiting for restocking.

### VIN lookup ?
Need to learn what it is and how to make use of it.  
https://vpic.nhtsa.dot.gov/api/ is a good provider for global/north american makers.  
It does not include French or Moroccan makers, like Renault, Dacia, PSA, ...  