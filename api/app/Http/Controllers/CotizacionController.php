<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class CotizacionController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $data = $request->all();
        $cotizacion = new \App\Cotizacion;
        $cotizacion->fill($data);
        if($cotizacion->save()) 
            return response()->json([
                'error' => false,
                'message' => 'Uploaded bro',
                'content' => $cotizacion
            ]);
        return response()->json([
                'error' => true,
                'message' => 'My bad',
                'content' => []
            ]);
        //dd($request);
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        $sql = "
            SELECT 
                AVG(beer/people) as beer
                ,AVG(bottles/people) as bottles
                ,AVG(costBeer/people) as costBeer
                ,AVG(costBottles/people) as costBottles
            FROM cotizacion
            GROUP BY userId
            HAVING userId = {$id}
        ";
        $cotizacion = DB::select($sql);
        if($cotizacion){
            $cotizacion = $cotizacion[0];
            $message_cotizacion = 'Based on previous data, average per person: Beers: '.$cotizacion->beer .' Bottles: '.$cotizacion->bottles .' Cost of beers: $'.$cotizacion->costBeer.' Cost of bottles: $'.$cotizacion->costBottles;
            return response()->json([
                'error' => false,
                'message' => $message_cotizacion,
                'content' => $cotizacion
            ]);
        }
        return response()->json([
                'error' => true,
                'message' => 'My bad',
                'content' => []
            ]);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}
