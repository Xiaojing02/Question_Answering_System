var NumberLocalizer = Class.create();

// Unit tests for this class are located in workspace/b2/grading/src/test/resources/blackboard/webapps/gradebook2/js/NumberLocalizerJSTest.html
// and run from NumberLocalizerJSTest.java
NumberLocalizer.prototype =
{
    DEFAULT_SCORE_MAX_FRACTION_DIGITS : 5, // Corresponds to GradeFormat.MAX_SCORE_DISPLAY_SCALE
    DEFAULT_SCORE_MIN_FRACTION_DIGITS : 2, // Corresponds to GradeFormat.MIN_SCORE_DISPLAY_SCALE
    DEFAULT_POINTS_MAX_FRACTION_DIGITS : 5, // Corresponds to GradeFormat.MAX_POINTS_DISPLAY_SCALE
    DEFAULT_POINTS_MIN_FRACTION_DIGITS : 0, // Corresponds to GradeFormat.MIN_POINTS_DISPLAY_SCALE

    initialize : function()
    {
      this.thousandsSeparator = ( typeof LOCALE_SETTINGS === 'undefined' || LOCALE_SETTINGS.getString('number_format.thousands_sep') === null ) ? ',' : LOCALE_SETTINGS.getString('number_format.thousands_sep');
      this.needToConvertThousands = ( this.thousandsSeparator !== ',' ) ? true : false;

      this.decimalSeparator = ( typeof LOCALE_SETTINGS === 'undefined' || LOCALE_SETTINGS.getString('number_format.decimal_point') === null ) ? '.' : LOCALE_SETTINGS.getString('number_format.decimal_point');
      this.needToConvertDecimal = ( this.decimalSeparator !== '.' ) ? true : false;
    },

    formatScore : function ( num, doTruncate )
    {
      return this.formatNumberWithRoundingMode( num, this.DEFAULT_SCORE_MIN_FRACTION_DIGITS, this.DEFAULT_SCORE_MAX_FRACTION_DIGITS, doTruncate );
    },

    formatPoints : function ( num, doTruncate )
    {
      return this.formatNumberWithRoundingMode( num, this.DEFAULT_POINTS_MIN_FRACTION_DIGITS, this.DEFAULT_POINTS_MAX_FRACTION_DIGITS, doTruncate );
    },

    /**
     * Format and the given number with the specified fraction digits and rounding mode.
     *
     * @param num Number to format. If string, assume already localized.
     * @param minFractionDigits Minimum number of digits after the decimal place
     * @param maxFractionDigits Maximum number of digits after the decimal place
     * @param doTruncate If true, truncate the number if there are more than maxFractionDigits. Otherwise, round. Defaults to true.
     * @returns A localized formatted numeric string
     */
    formatNumberWithRoundingMode : function( num, minFractionDigits, maxFractionDigits, doTruncate )
    {
      //only parse if num is already localized (i.e. in string format)
      var numParsed = ( typeof num === "string" ) ? this.parseNumber( num ) : num;
      if( isNaN( numParsed ) )
      {
        return num.toString();
      }

      minFractionDigits = parseInt( minFractionDigits, 10 );
      maxFractionDigits = parseInt( maxFractionDigits, 10 );

      // if invalid minFractionDigits, assume min 0
      if( isNaN( minFractionDigits ) || minFractionDigits < 0 )
      {
        minFractionDigits = 0;
      }

      if( isNaN( maxFractionDigits ) )
      {
        var roundedToMin = numParsed.toFixed( minFractionDigits );
        if( parseFloat( roundedToMin ) === numParsed )
        {
          // toFixed only added trailing zeroes, so use this value
          return this.formatNumber( roundedToMin )
        }
        else
        {
          return this.formatNumber( numParsed );
        }
      }

      // If invalid range, min overrides max
      if( maxFractionDigits < minFractionDigits )
      {
        maxFractionDigits = minFractionDigits;
      }

      if( doTruncate === undefined )
      {
        doTruncate = true;
      }

      if( doTruncate )
      {
        return this._formatNumberTruncate( numParsed, minFractionDigits, maxFractionDigits );
      }
      else
      {
        return this._formatNumberRound( numParsed, minFractionDigits, maxFractionDigits );
      }

    },

    /**
     * Format and localize the given number, truncating if needed
     * @param num Number to format - must be of type Number
     * @param minFractionDigits Minimum number of digits after the decimal place. Non-optional, must be a non-negative Integer,
     *  less than or equal to maxFractionDigits
     * @param maxFractionDigits Maximum number of digits after the decimal place. If num has more than maxFractionDigits
     *  decimal places, the output will be truncated. Non-optional, must be a non-negative Integer, greater than or equal
     *  to minFractionDigits
     * @returns A localized formatted numeric string
     */
    _formatNumberTruncate : function(num, minFractionDigits, maxFractionDigits )
    {
      // Capture group 1: integer digits
      // 2: optional fractional part up to maxFractionDigits digits, with decimal point
      // 3 (contained in 2): optional fractional part up to maxFractionDigits digits, without decimal point
      if( maxFractionDigits === 0 || maxFractionDigits === 1 )
      {
        var re = new RegExp("^([-]?[\\d,]+)(\\.([1-9]))?");
      }
      else
      {
        var re = new RegExp("^([-]?[\\d,]+)(\\.(\\d{0," + (maxFractionDigits - 1) + "}[1-9]))?");
      }

      var splitRegexMatch = num.toString().match(re);

      if( !splitRegexMatch )
      {
        return this.formatNumber( num );
      }

      // Don't want fractional part, or don't need a fractional part and no fractional digits found
      if( maxFractionDigits === 0 || ( minFractionDigits === 0 && !splitRegexMatch[3] ) )
      {
        return splitRegexMatch[1] ? this.formatNumber(splitRegexMatch[1]) : "";
      }

      var integerPart = splitRegexMatch[1] ? splitRegexMatch[1] : "0";
      var fractionalPart = splitRegexMatch[3] ? splitRegexMatch[3] : "";

      if( fractionalPart.length < minFractionDigits )
      {
        var numZeroesToPad = minFractionDigits - fractionalPart.length;

        var padding = Array( numZeroesToPad + 1 ).join("0");

        fractionalPart = fractionalPart + padding;
      }

      return this.formatNumber( integerPart + "." + fractionalPart );
    },

    /**
     * Format and localize the given number, truncating if needed
     * @param num Number to format - must be of type Number
     * @param minFractionDigits Minimum number of digits after the decimal place. Non-optional, must be a non-negative Integer,
     *  less than or equal to maxFractionDigits
     * @param maxFractionDigits Maximum number of digits after the decimal place. If num has more than maxFractionDigits
     *  decimal places, the output will be rounded. Non-optional, must be a non-negative Integer, greater than or equal
     *  to minFractionDigits
     * @returns A localized formatted numeric string
     */
    _formatNumberRound : function(num, minFractionDigits, maxFractionDigits )
    {
      // Logic moved from gradebook_utils.js
      // now will try to get as little extra digits as needed, up to maxFractionDigits
      var roundBase = Math.pow( 10, minFractionDigits );
      var maxRoundBase = Math.pow( 10, maxFractionDigits );
      var mostPreciseRounding = Math.round( num * maxRoundBase ) / maxRoundBase;

      for ( var i = minFractionDigits; i < maxFractionDigits; ++i )
      {
        var floatRound = Math.round( num * roundBase ) / roundBase;
        roundBase *= 10;
        if ( floatRound == mostPreciseRounding )
        {
          // adding any more digit will not add any more precision
          return this.formatNumber( num.toFixed( i ) );
        }
      }
      return this.formatNumber( num.toFixed( maxFractionDigits ) );
    },

    // Takes a number that is unlocalized and converts it to
    // the current locale format.
    formatNumber : function( f )
    {
      var result;
      result = f.toString();

      // Replace and thousands delimiter with a token so we can
      // replace it with the final symbol after we replace the decimal symbol.
      if ( this.needToConvertThousands )
      {
        result = result.replace( ',', '[comma]' );
      }

      if ( this.needToConvertDecimal )
      {
        result = result.replace( '.', this.decimalSeparator );
      }

      if ( this.needToConvertThousands )
      {
        result = result.replace( '[comma]', this.thousandsSeparator );
      }

      return result;
    },

    // Takes a number that is in the current locale format and
    // converts it back to an unlocalized number.
    parseNumber : function( num )
    {
      var result;
      result = num.toString();

      // Parsing string to return as a float, so we don't need the thousands
      // separator anymore.
      result = result.replace( this.thousandsSeparator, '' );

      if ( this.needToConvertDecimal )
      {
        result = result.replace( this.decimalSeparator, '.' );
      }

      return parseFloat( result );
    }
};
