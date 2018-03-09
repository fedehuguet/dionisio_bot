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
                'message' => 'Guardado compa',
                'content' => $cotizacion
            ]);
        return response()->json([
                'error' => true,
                'message' => 'No se que paso bro',
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
            $message_cotizacion = 'Con base a tus fiestas anteriores, promedio por persona: Cervezas: '.$cotizacion->beer .' Botellas: '.$cotizacion->bottles .' Gasto en cervezas: $'.$cotizacion->costBeer.' Gasto en botellas: $'.$cotizacion->costBottles;
            return response()->json([
                'error' => false,
                'message' => $message_cotizacion,
                'content' => $cotizacion
            ]);
        }
        return response()->json([
                'error' => true,
                'message' => 'No se que paso bro',
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
