@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div class="col-md-12">
        	<div class="panel panel-default">
        		<div class="panel-heading">Add Member</div>
        		<div class="panel-body">
                    {{ Form::model($member, ['action' => 'MemberController@store', 'class' => 'form-horizontal']) }}
                        
                        <div class="form-group{{ $errors->has('name') ? ' has-error' : '' }}">
                            {{ Form::label('name', 'Name', ['class' => 'col-md-4 control-label']) }}

                            <div class="col-md-6">
                                {{ Form::text('name', '', ['class' => 'form-control']) }}

                                @if ($errors->has('name'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('name') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group{{ $errors->has('email') ? ' has-error' : '' }}">
                            {{ Form::label('email', 'Email', ['class' => 'col-md-4 control-label']) }}

                            <div class="col-md-6">
                                {{ Form::email('email', '', ['class' => 'form-control']) }}
                                
                                @if ($errors->has('email'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('email') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group{{ $errors->has('payment_provider_id') ? ' has-error' : '' }}">
                            {{ Form::label('payment_provider_id', 'Payment Via', ['class' => 'col-md-4 control-label']) }}

                            <div class="col-md-6">
                                {{ Form::select('payment_provider_id', $providers, 2, ['class' => 'form-control']) }}

                                

                                @if ($errors->has('payment_provider_id'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('payment_provider_id') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group{{ $errors->has('member_tier_id') ? ' has-error' : '' }}">
                            {{ Form::label('member_tier_id', 'Membership Tier', ['class' => 'col-md-4 control-label']) }}
                                                        
                            <div class="col-md-6">
                                {{ Form::select('member_tier_id', $tiers, 2, ['class' => 'form-control']) }}

                                @if ($errors->has('member_tier_id'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('member_tier_id') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group{{ $errors->has('expire_date') ? ' has-error' : '' }}">
                            {{ Form::label('expire_date', 'Membership Expiration Date', ['class' => 'col-md-4 control-label']) }}
                                                        
                            <div class="col-md-6">
                                {{ Form::text('expire_date', null, ['class' => 'form-control datepicker']) }}

                                @if ($errors->has('expire_date'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('expire_date') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group{{ $errors->has('rfid') ? ' has-error' : '' }}">
                            <label for="rfid" class="col-md-4 control-label">rfid</label>

                            <div class="col-md-6">
                                {{ Form::text('rfid', '', ['class' => 'form-control']) }}

                                @if ($errors->has('rfid'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('rfid') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>
                        
            			<div class="row">
            				<div class="col-md-12 text-right">
            					<a class="btn btn-default" href="{{ url('/members') }}">Cancel</a>
                                <button type="submit" class="btn btn-primary">Submit</button>
            				</div>
            			</div>

                    {{ Form::close() }}
                    
        		</div>
        	</div>
        </div>
    </div>
</div>
@endsection
