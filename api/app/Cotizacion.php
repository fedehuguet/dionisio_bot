<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Cotizacion extends Model
{
    protected $table = 'cotizacion';
    protected $primaryKey = 'id';
    protected $fillable = [
        'userId','beer','bottles','costBeer','costBottles','people'
    ];
}
